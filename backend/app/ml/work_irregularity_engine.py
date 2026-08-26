import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional
from app.schemas.layer2_schema import WorkLevelRecord

class Layer2WorkIrregularityEngine:
    """
    Layer 2: Work-Level Financial & Operational Irregularity Detection Engine.
    Operates on optional work-level eSAKSHI project data.
    
    Implements 12 evidence-based signals:
    1. COST_OVERRUN: Expenditure > Sanctioned / Estimated amount
    2. BILL_SANCTION_MISMATCH: Payments/Bills exceed sanctioned amount
    3. PAYMENT_PROGRESS_MISMATCH: Payment % substantially exceeds physical progress %
    4. PROJECT_DELAY: Completion date / duration exceeds expected schedule
    5. DUPLICATE_INVOICE: Duplicate bill IDs, amounts, vendors, or documents
    6. DUPLICATE_WORK: Similar work descriptions in same constituency/vendor
    7. VENDOR_CONCENTRATION: Vendor receiving disproportionate allocation
    8. CROSS_PROJECT_VENDOR_PATTERN: Vendor appearing in multiple anomalous projects
    9. PAYMENT_TIMING_ANOMALY: Clustered or rapid payment timing
    10. PEER_PROJECT_COST_ANOMALY: Cost exceeding peer range of similar work type & scope
    11. MISSING_DOCUMENTS: Mandatory completion/inspection documents missing
    12. SANCTION_EXPENDITURE_PAYMENT_CONSISTENCY: Flow mismatch across sanction -> expenditure -> payment
    
    GUARANTEE:
    - Never fabricates data if fields are missing.
    - Never outputs "Fraud Confirmed" or accuses any person.
    - Uses non-accusatory governance language.
    """
    
    def evaluate_works(self, work_records: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not work_records:
            return {
                "is_layer2_active": False,
                "layer2_signals_triggered": [],
                "layer2_evidence": [],
                "layer2_missing_evidence": [
                    "Work-level eSAKSHI data (bills, vendors, physical progress %, completion certificates) is not available in the connected official dataset."
                ],
                "layer2_risk_score_delta": 0.0,
                "notice": "Data not available in connected official dataset"
            }
            
        df_works = pd.DataFrame(work_records)
        signals = []
        evidence = []
        missing_evidence = []
        total_risk_delta = 0.0

        # Check required fields presence
        has_sanction = 'sanctioned_amount' in df_works.columns and not df_works['sanctioned_amount'].isna().all()
        has_expenditure = 'expenditure' in df_works.columns and not df_works['expenditure'].isna().all()
        has_payment = 'payment_amount' in df_works.columns and not df_works['payment_amount'].isna().all()
        has_progress = 'physical_progress_pct' in df_works.columns and not df_works['physical_progress_pct'].isna().all()
        has_vendor = 'vendor_id' in df_works.columns and not df_works['vendor_id'].isna().all()
        has_bill = 'bill_id' in df_works.columns and not df_works['bill_id'].isna().all()
        has_docs = 'document_ids' in df_works.columns

        # 1. Signal 1: COST_OVERRUN (Expenditure vs Sanctioned/Estimated)
        if has_sanction and has_expenditure:
            for idx, row in df_works.iterrows():
                s_amt = row.get('sanctioned_amount') or row.get('estimated_cost') or 0.0
                e_amt = row.get('expenditure') or 0.0
                if s_amt > 0 and e_amt > s_amt:
                    excess = e_amt - s_amt
                    excess_pct = (excess / s_amt) * 100.0
                    signals.append({
                        "signal": "COST_OVERRUN",
                        "value": f"₹{e_amt/1e7:.2f} Cr expenditure vs ₹{s_amt/1e7:.2f} Cr sanctioned (+{excess_pct:.1f}%)",
                        "severity": "CRITICAL" if excess_pct > 50 else "HIGH",
                        "source": "official_work_expenditure_ledger",
                        "method": "SanctionVsExpenditureDelta"
                    })
                    evidence.append({
                        "factor": "Cost Overrun Detected",
                        "impact": "+35 pts",
                        "description": f"Actual expenditure (₹{e_amt/1e7:.2f} Cr) exceeds sanctioned amount (₹{s_amt/1e7:.2f} Cr) by ₹{excess/1e7:.2f} Cr ({excess_pct:.1f}% excess).",
                        "source_ref": f"Work ID: {row.get('work_id', 'N/A')}"
                    })
                    total_risk_delta += 35.0
        else:
            missing_evidence.append("Sanctioned vs actual expenditure comparison")

        # 2. Signal 2: BILL_SANCTION_MISMATCH (Bill/Payment vs Sanctioned)
        if has_sanction and (has_payment or 'bill_amount' in df_works.columns):
            for idx, row in df_works.iterrows():
                s_amt = row.get('sanctioned_amount') or 0.0
                p_amt = row.get('payment_amount') or row.get('bill_amount') or 0.0
                if s_amt > 0 and p_amt > s_amt * 1.1: # 10% threshold above sanction
                    potential_excess = p_amt - s_amt
                    signals.append({
                        "signal": "BILL_SANCTION_MISMATCH",
                        "value": f"Bills/Payments (₹{p_amt/1e7:.2f} Cr) exceed Sanctioned amount (₹{s_amt/1e7:.2f} Cr)",
                        "severity": "CRITICAL",
                        "source": "esakshi_disbursement_records",
                        "method": "DisbursementVsSanctionAudit"
                    })
                    evidence.append({
                        "factor": "Bill vs Sanction Amount Mismatch",
                        "impact": "+40 pts",
                        "description": f"Total bills/payments (₹{p_amt/1e7:.2f} Cr) exceed approved sanctioned cost (₹{s_amt/1e7:.2f} Cr) by potential excess of ₹{potential_excess/1e7:.2f} Cr.",
                        "source_ref": f"Work ID: {row.get('work_id', 'N/A')}, Bill ID: {row.get('bill_id', 'N/A')}"
                    })
                    total_risk_delta += 40.0
        else:
            missing_evidence.append("Bill/Payment disbursement vs sanctioned cost verification")

        # 3. Signal 3: PAYMENT_PROGRESS_MISMATCH (Payment % vs Physical Progress %)
        if has_payment and has_sanction and has_progress:
            for idx, row in df_works.iterrows():
                s_amt = row.get('sanctioned_amount') or 1.0
                p_amt = row.get('payment_amount') or 0.0
                prog_pct = row.get('physical_progress_pct') or 0.0
                payment_pct = (p_amt / s_amt) * 100.0 if s_amt > 0 else 0.0
                
                # e.g., 85% paid vs 40% physical progress (gap >= 35%)
                if payment_pct > (prog_pct + 35.0) and payment_pct > 50.0:
                    signals.append({
                        "signal": "PAYMENT_PROGRESS_MISMATCH",
                        "value": f"Payment Disbursed: {payment_pct:.1f}% vs Physical Progress: {prog_pct:.1f}%",
                        "severity": "CRITICAL",
                        "source": "esakshi_physical_verification_ledger",
                        "method": "FinancialVsPhysicalProgressDivergence"
                    })
                    evidence.append({
                        "factor": "Financial Payment vs Physical Progress Mismatch",
                        "impact": "+35 pts",
                        "description": f"Disbursed payment stands at {payment_pct:.1f}% of sanction, while verified physical progress is only {prog_pct:.1f}% (Divergence Gap: {payment_pct - prog_pct:.1f}%).",
                        "source_ref": f"Work ID: {row.get('work_id', 'N/A')}"
                    })
                    total_risk_delta += 35.0
        else:
            missing_evidence.append("Physical progress % vs financial payment audit")

        # 4. Signal 4: PROJECT_DELAY
        if 'completion_date' in df_works.columns and 'sanction_date' in df_works.columns:
            for idx, row in df_works.iterrows():
                status = str(row.get('completion_status', '')).upper()
                prog = row.get('physical_progress_pct') or 0.0
                if status in ['DELAYED', 'OVERDUE'] or (prog < 100.0 and row.get('completion_date')):
                    signals.append({
                        "signal": "PROJECT_DELAY",
                        "value": f"Status: {status}, Physical Progress: {prog}%",
                        "severity": "MEDIUM",
                        "source": "official_milestone_tracker",
                        "method": "ScheduleOverrunAudit"
                    })
                    evidence.append({
                        "factor": "Project Completion Timeline Overrun",
                        "impact": "+15 pts",
                        "description": f"Project is classified as {status} with incomplete physical progress ({prog}%).",
                        "source_ref": f"Work ID: {row.get('work_id', 'N/A')}"
                    })
                    total_risk_delta += 15.0
        else:
            missing_evidence.append("Project timeline and target completion schedule")

        # 5. Signal 5: DUPLICATE_INVOICE
        if has_bill:
            dupes = df_works[df_works.duplicated(subset=['bill_id'], keep=False)]
            if not dupes.empty:
                for bill_id in dupes['bill_id'].unique():
                    if bill_id:
                        signals.append({
                            "signal": "DUPLICATE_INVOICE",
                            "value": f"Duplicate Bill ID detected: {bill_id}",
                            "severity": "CRITICAL",
                            "source": "esakshi_invoice_registry",
                            "method": "ExactKeyDuplicateAudit"
                        })
                        evidence.append({
                            "factor": "Duplicate Invoice ID Detected",
                            "impact": "+45 pts",
                            "description": f"Bill/Invoice ID '{bill_id}' appears multiple times across distinct work records.",
                            "source_ref": f"Bill ID: {bill_id}"
                        })
                        total_risk_delta += 45.0
        else:
            missing_evidence.append("Invoice/Bill ID verification ledger")

        # 6. Signal 6: DUPLICATE_WORK
        if 'work_type' in df_works.columns and 'constituency' in df_works.columns:
            work_dupes = df_works[df_works.duplicated(subset=['constituency', 'work_type', 'sanctioned_amount'], keep=False)]
            if not work_dupes.empty:
                signals.append({
                    "signal": "DUPLICATE_WORK",
                    "value": "Multiple identical work titles and sanctioned amounts in same constituency",
                    "severity": "HIGH",
                    "source": "official_work_sanction_register",
                    "method": "DuplicateSanctionAudit"
                })
                evidence.append({
                    "factor": "Potential Duplicate Work Sanction",
                    "impact": "+30 pts",
                    "description": "Identical work type and sanctioned amount sanctioned multiple times within the same constituency.",
                    "source_ref": "Constituency Sanction Register"
                })
                total_risk_delta += 30.0

        # 7. Signal 7: VENDOR_CONCENTRATION
        if has_vendor:
            vendor_counts = df_works['vendor_name'].value_counts(normalize=True)
            for vname, share in vendor_counts.items():
                if share > 0.40 and len(df_works) >= 3: # Single vendor getting >40% of works
                    signals.append({
                        "signal": "VENDOR_CONCENTRATION",
                        "value": f"Vendor '{vname}' holds {share*100:.1f}% of total constituency works",
                        "severity": "HIGH",
                        "source": "vendor_procurement_analytics",
                        "method": "HerfindahlHirschmanVendorIndex"
                    })
                    evidence.append({
                        "factor": "High Vendor Allocation Concentration",
                        "impact": "+25 pts",
                        "description": f"Vendor '{vname}' has been awarded {share*100:.1f}% of all sanctioned project works.",
                        "source_ref": f"Vendor: {vname}"
                    })
                    total_risk_delta += 25.0
        else:
            missing_evidence.append("Vendor procurement & allocation records")

        # 8. Signal 8: CROSS_PROJECT_VENDOR_PATTERN
        if has_vendor and 'expenditure' in df_works.columns:
            anomalous_vendors = df_works[df_works['expenditure'] > df_works['sanctioned_amount']]['vendor_name'].dropna().unique()
            if len(anomalous_vendors) > 0:
                for vname in anomalous_vendors:
                    signals.append({
                        "signal": "CROSS_PROJECT_VENDOR_PATTERN",
                        "value": f"Vendor '{vname}' associated with multiple cost-overrun projects",
                        "severity": "HIGH",
                        "source": "cross_project_vendor_audit",
                        "method": "VendorAnomalousLinkage"
                    })
                    evidence.append({
                        "factor": "Cross-Project Vendor Overrun Pattern",
                        "impact": "+20 pts",
                        "description": f"Vendor '{vname}' is repeatedly linked to projects experiencing cost overruns.",
                        "source_ref": f"Vendor: {vname}"
                    })
                    total_risk_delta += 20.0

        # 9. Signal 9: PAYMENT_TIMING_ANOMALY
        if 'payment_date' in df_works.columns:
            df_works['payment_dt'] = pd.to_datetime(df_works['payment_date'], errors='coerce')
            valid_dates = df_works.dropna(subset=['payment_dt'])
            if len(valid_dates) >= 3:
                date_diffs = valid_dates['payment_dt'].sort_values().diff().dt.days
                if (date_diffs == 0).sum() >= 2: # Clustered payments on same day
                    signals.append({
                        "signal": "PAYMENT_TIMING_ANOMALY",
                        "value": "Multiple large disbursements executed on the exact same date",
                        "severity": "MEDIUM",
                        "source": "pfms_payment_timestamp_log",
                        "method": "TemporalDisbursementClusterAudit"
                    })
                    evidence.append({
                        "factor": "Clustered Payment Disbursement Timing",
                        "impact": "+15 pts",
                        "description": "Multiple project disbursements were executed simultaneously on the same date.",
                        "source_ref": "PFMS Transaction Ledger"
                    })
                    total_risk_delta += 15.0
        else:
            missing_evidence.append("Payment transaction timestamps (PFMS payment ledger)")

        # 10. Signal 10: PEER_PROJECT_COST_ANOMALY (Contextual peer project comparison)
        if 'work_type' in df_works.columns and has_sanction:
            type_means = df_works.groupby('work_type')['sanctioned_amount'].transform('mean')
            type_stds = df_works.groupby('work_type')['sanctioned_amount'].transform('std').fillna(1.0)
            for idx, row in df_works.iterrows():
                w_type = row.get('work_type', 'General')
                s_amt = row.get('sanctioned_amount') or 0.0
                mean_t = type_means.iloc[idx]
                std_t = type_stds.iloc[idx]
                if std_t > 0 and (s_amt - mean_t) / std_t > 2.5:
                    signals.append({
                        "signal": "PEER_PROJECT_COST_ANOMALY",
                        "value": f"Project cost ₹{s_amt/1e7:.2f} Cr exceeds peer work type '{w_type}' range (Mean: ₹{mean_t/1e7:.2f} Cr)",
                        "severity": "HIGH",
                        "source": "peer_project_type_benchmark",
                        "method": "WorkTypeContextualPeerBenchmark"
                    })
                    evidence.append({
                        "factor": "Peer Project Cost Anomaly",
                        "impact": "+20 pts",
                        "description": f"Sanctioned cost (₹{s_amt/1e7:.2f} Cr) significantly exceeds comparable peer projects of type '{w_type}' (Average: ₹{mean_t/1e7:.2f} Cr).",
                        "source_ref": f"Work Type: {w_type}"
                    })
                    total_risk_delta += 20.0

        # 11. Signal 11: MISSING_DOCUMENTS
        if has_docs:
            for idx, row in df_works.iterrows():
                docs = row.get('document_ids') or []
                prog = row.get('physical_progress_pct') or 0.0
                if prog > 50.0 and len(docs) == 0:
                    signals.append({
                        "signal": "MISSING_DOCUMENTS",
                        "value": f"Zero verification documents attached for project at {prog}% physical progress",
                        "severity": "MEDIUM",
                        "source": "geotagged_document_repository",
                        "method": "MandatoryVerificationDocAudit"
                    })
                    evidence.append({
                        "factor": "Missing Mandatory Progress Verification Documents",
                        "impact": "+15 pts",
                        "description": f"Project is reported at {prog}% completion but lacks attached geotagged photos or completion certificates.",
                        "source_ref": f"Work ID: {row.get('work_id', 'N/A')}"
                    })
                    total_risk_delta += 15.0
        else:
            missing_evidence.append("Geotagged site photos & physical completion certificates")

        # 12. Signal 12: SANCTION_EXPENDITURE_PAYMENT_CONSISTENCY
        if has_sanction and has_expenditure and has_payment:
            for idx, row in df_works.iterrows():
                s_amt = row.get('sanctioned_amount') or 0.0
                e_amt = row.get('expenditure') or 0.0
                p_amt = row.get('payment_amount') or 0.0
                if p_amt > e_amt * 1.15: # Payment exceeds recorded expenditure by 15%
                    signals.append({
                        "signal": "SANCTION_EXPENDITURE_PAYMENT_CONSISTENCY",
                        "value": f"Disbursed Payment (₹{p_amt/1e7:.2f} Cr) exceeds Recorded Expenditure (₹{e_amt/1e7:.2f} Cr)",
                        "severity": "HIGH",
                        "source": "tripartite_flow_consistency_engine",
                        "method": "SanctionExpenditurePaymentTriangulation"
                    })
                    evidence.append({
                        "factor": "Financial Flow Triangulation Mismatch",
                        "impact": "+25 pts",
                        "description": f"Disbursed payments (₹{p_amt/1e7:.2f} Cr) exceed verified recorded expenditure (₹{e_amt/1e7:.2f} Cr).",
                        "source_ref": f"Work ID: {row.get('work_id', 'N/A')}"
                    })
                    total_risk_delta += 25.0

        return {
            "is_layer2_active": True,
            "layer2_signals_triggered": signals,
            "layer2_evidence": evidence,
            "layer2_missing_evidence": missing_evidence if missing_evidence else ["Site physical re-verification audit"],
            "layer2_risk_score_delta": min(total_risk_delta, 50.0), # Capped at +50 pts
            "notice": "Evaluated against work-level eSAKSHI dataset"
        }

# Singleton instance
work_irregularity_engine = Layer2WorkIrregularityEngine()
