import os
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional

CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "Allocated_Limit_for_Honble_MPs.csv")

class RealDataService:
    """
    Official MPLADS Data Ingestion & Analytics Service.
    Strictly reads and processes Allocated_Limit_for_Honble_MPs.csv without mixing simulated data.
    """
    
    def __init__(self, csv_filepath: str = CSV_PATH):
        self.csv_filepath = csv_filepath
        self.df_raw: pd.DataFrame = None
        self.df_mp: pd.DataFrame = None
        self.grand_total_str: str = ""
        self._load_and_validate()

    def _load_and_validate(self):
        if not os.path.exists(self.csv_filepath):
            raise FileNotFoundError(f"Official CSV dataset not found at {self.csv_filepath}")
            
        self.df_raw = pd.read_csv(self.csv_filepath)
        
        # Extract Grand Total row if present
        gt_mask = self.df_raw['Sr. No.'].astype(str).str.contains('Grand Total', case=False, na=False)
        if gt_mask.any():
            self.grand_total_str = str(self.df_raw[gt_mask]['Allocated AMOUNT ( ₹ )'].values[0])
            self.df_mp = self.df_raw[~gt_mask].copy()
        else:
            self.df_mp = self.df_raw.copy()

        # Clean numeric allocation column
        self.df_mp['allocated_amount_clean'] = (
            self.df_mp['Allocated AMOUNT ( ₹ )']
            .astype(str)
            .str.replace(',', '')
            .str.strip()
        )
        self.df_mp['allocated_amount'] = pd.to_numeric(self.df_mp['allocated_amount_clean'], errors='coerce')
        
        # Standardized column names
        self.df_mp['sr_no'] = self.df_mp['Sr. No.'].astype(str)
        self.df_mp['state'] = self.df_mp['State'].astype(str).str.strip()
        self.df_mp['mp_name'] = self.df_mp["Hon'ble Members of Parliaments"].astype(str).str.strip()
        self.df_mp['constituency'] = self.df_mp['Constituency'].astype(str).str.strip()
        
        # Standard category flags
        self.df_mp['is_sc'] = self.df_mp['constituency'].str.contains('(SC)', regex=False)
        self.df_mp['is_st'] = self.df_mp['constituency'].str.contains('(ST)', regex=False)
        self.df_mp['is_general'] = ~self.df_mp['is_sc'] & ~self.df_mp['is_st']
        
        # Generate internal ID for each MP
        self.df_mp['mp_id'] = ["MP_" + str(i + 1).zfill(3) for i in range(len(self.df_mp))]

    def get_summary_kpis(self) -> Dict[str, Any]:
        """Calculates real national KPIs directly from dataset."""
        valid_series = self.df_mp['allocated_amount'].dropna()
        return {
            "total_mp_records": int(len(self.df_mp)),
            "valid_allocation_records": int(valid_series.count()),
            "missing_allocation_records": int(self.df_mp['allocated_amount'].isna().sum()),
            "total_allocation_inr": float(valid_series.sum()),
            "total_allocation_crores": round(float(valid_series.sum()) / 1e7, 2),
            "mean_allocation_inr": float(valid_series.mean()),
            "median_allocation_inr": float(valid_series.median()),
            "min_allocation_inr": float(valid_series.min()),
            "max_allocation_inr": float(valid_series.max()),
            "std_dev_inr": float(valid_series.std()),
            "unique_states_count": int(self.df_mp['state'].nunique()),
            "unique_constituencies_count": int(self.df_mp['constituency'].nunique()),
            "baseline_mp_count_14_7cr": int((valid_series == 147000000).sum()),
            "official_grand_total_csv_string": self.grand_total_str
        }

    def get_state_analytics(self) -> List[Dict[str, Any]]:
        """Returns aggregated state-wise analytics derived from real CSV."""
        grouped = self.df_mp.groupby('state')
        states_list = []
        for state_name, group in grouped:
            valid_amt = group['allocated_amount'].dropna()
            states_list.append({
                "state": state_name,
                "mp_count": int(len(group)),
                "valid_mp_count": int(valid_amt.count()),
                "missing_mp_count": int(group['allocated_amount'].isna().sum()),
                "total_allocation_inr": float(valid_amt.sum()) if not valid_amt.empty else 0.0,
                "total_allocation_crores": round(float(valid_amt.sum()) / 1e7, 2) if not valid_amt.empty else 0.0,
                "mean_allocation_inr": float(valid_amt.mean()) if not valid_amt.empty else 0.0,
                "min_allocation_inr": float(valid_amt.min()) if not valid_amt.empty else 0.0,
                "max_allocation_inr": float(valid_amt.max()) if not valid_amt.empty else 0.0,
                "baseline_14_7cr_count": int((valid_amt == 147000000).sum()),
                "deviating_allocation_count": int((valid_amt != 147000000).sum())
            })
        # Sort by total allocation descending
        states_list.sort(key=lambda x: x['total_allocation_inr'], reverse=True)
        return states_list

    def get_all_mps(
        self, 
        state_filter: Optional[str] = None, 
        search: Optional[str] = None,
        outlier_only: bool = False,
        limit: int = 600,
        offset: int = 0
    ) -> Dict[str, Any]:
        """Returns list of MPs with filtering and pagination."""
        df_filtered = self.df_mp.copy()
        
        if state_filter and state_filter.lower() != "all":
            df_filtered = df_filtered[df_filtered['state'].str.lower() == state_filter.lower()]
            
        if search:
            q = search.lower()
            df_filtered = df_filtered[
                df_filtered['mp_name'].str.lower().str.contains(q) |
                df_filtered['constituency'].str.lower().str.contains(q) |
                df_filtered['state'].str.lower().str.contains(q)
            ]
            
        if outlier_only:
            df_filtered = df_filtered[df_filtered['allocated_amount'] != 147000000]

        total_matches = len(df_filtered)
        paginated_df = df_filtered.iloc[offset:offset+limit]
        
        records = []
        for _, row in paginated_df.iterrows():
            amt = row['allocated_amount']
            is_missing = pd.isna(amt)
            records.append({
                "mp_id": row['mp_id'],
                "sr_no": row['sr_no'],
                "state": row['state'],
                "mp_name": row['mp_name'],
                "constituency": row['constituency'],
                "allocated_amount_inr": float(amt) if not is_missing else None,
                "allocated_amount_crores": round(float(amt) / 1e7, 2) if not is_missing else None,
                "is_missing": is_missing,
                "is_baseline": (amt == 147000000) if not is_missing else False,
                "deviation_from_baseline_inr": float(amt - 147000000) if not is_missing else None,
                "category": "ST" if row['is_st'] else ("SC" if row['is_sc'] else "General")
            })
            
        return {
            "total_count": total_matches,
            "limit": limit,
            "offset": offset,
            "mps": records
        }

    def get_mp_by_id(self, mp_id: str) -> Optional[Dict[str, Any]]:
        row = self.df_mp[self.df_mp['mp_id'] == mp_id]
        if row.empty:
            return None
        r = row.iloc[0]
        amt = r['allocated_amount']
        is_missing = pd.isna(amt)
        return {
            "mp_id": r['mp_id'],
            "sr_no": r['sr_no'],
            "state": r['state'],
            "mp_name": r['mp_name'],
            "constituency": r['constituency'],
            "allocated_amount_inr": float(amt) if not is_missing else None,
            "allocated_amount_crores": round(float(amt) / 1e7, 2) if not is_missing else None,
            "is_missing": is_missing,
            "is_baseline": (amt == 147000000) if not is_missing else False,
            "deviation_from_baseline_inr": float(amt - 147000000) if not is_missing else None,
            "category": "ST" if r['is_st'] else ("SC" if r['is_sc'] else "General")
        }

# Singleton instance
real_data_service = RealDataService()
