import os
import hashlib
import json
import urllib.parse
import psycopg2
from psycopg2.extras import RealDictCursor
import pandas as pd
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

# Load environment variables from .env / backend/.env
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env"))
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

DATABASE_URL = os.getenv("DATABASE_URL", "")

if DATABASE_URL:
    url_clean = DATABASE_URL
    if "?" in url_clean:
        url_base, query_params = url_clean.split("?", 1)
    else:
        url_base, query_params = url_clean, ""

    url_no_scheme = url_base.replace("postgresql://", "").replace("postgres://", "")
    
    if "@" in url_no_scheme:
        user_pass, host_db = url_no_scheme.split("@", 1)
        if ":" in user_pass:
            raw_u, raw_p = user_pass.split(":", 1)
            PG_USER = urllib.parse.unquote(raw_u)
            PG_PASSWORD = urllib.parse.unquote(raw_p)
        else:
            PG_USER = urllib.parse.unquote(user_pass)
            PG_PASSWORD = ""
    else:
        PG_USER = urllib.parse.unquote(os.getenv("PG_USER", "swapnil"))
        PG_PASSWORD = urllib.parse.unquote(os.getenv("PG_PASSWORD", ""))
        host_db = url_no_scheme

    if "/" in host_db:
        host_port, PG_DBNAME = host_db.split("/", 1)
    else:
        host_port, PG_DBNAME = host_db, os.getenv("PG_DBNAME", "mplads_db")

    if ":" in host_port:
        PG_HOST, port_str = host_port.split(":", 1)
        PG_PORT = int(port_str)
    else:
        PG_HOST, PG_PORT = host_port, int(os.getenv("PG_PORT", "5432"))

    if PG_HOST not in ["localhost", "127.0.0.1"]:
        PG_SSLMODE = os.getenv("PG_SSLMODE", "require")
    else:
        PG_SSLMODE = os.getenv("PG_SSLMODE", "prefer")
else:
    PG_HOST = os.getenv("PG_HOST", "localhost")
    PG_PORT = int(os.getenv("PG_PORT", "5432"))
    PG_USER = urllib.parse.unquote(os.getenv("PG_USER", "swapnil"))
    PG_PASSWORD = urllib.parse.unquote(os.getenv("PG_PASSWORD", ""))
    PG_DBNAME = os.getenv("PG_DBNAME", "mplads_db")
    PG_SSLMODE = os.getenv("PG_SSLMODE", "prefer")

CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "data", "Allocated_Limit_for_Honble_MPs.csv")

class MPLADSDatabase:
    """
    Production Cloud PostgreSQL Relational Engine for MPLADS Command Center.
    Supports local PostgreSQL and cloud hosted PostgreSQL (Supabase / Neon / AWS RDS)
    with SSL/TLS security, idempotent CSV ingestion, dataset versioning,
    model run persistence, pre-computed anomaly signals, RBAC roles, and audit logging.
    """
    def __init__(self):
        self._init_db()

    def get_connection(self):
        conn_kwargs = {
            "dbname": PG_DBNAME,
            "user": PG_USER,
            "host": PG_HOST,
            "port": PG_PORT,
            "sslmode": PG_SSLMODE
        }
        if PG_PASSWORD:
            conn_kwargs["password"] = PG_PASSWORD

        conn = psycopg2.connect(**conn_kwargs)
        return conn

    def _init_db(self):
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                # Table 1: Dataset Versions
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS dataset_versions (
                        version_id SERIAL PRIMARY KEY,
                        version_tag VARCHAR(100) NOT NULL UNIQUE,
                        checksum_sha256 VARCHAR(100) NOT NULL,
                        source_filename VARCHAR(255) NOT NULL,
                        total_records INTEGER NOT NULL,
                        valid_records INTEGER NOT NULL,
                        missing_records INTEGER NOT NULL,
                        total_allocation_inr DOUBLE PRECISION NOT NULL,
                        ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)

                # Table 2: MP Allocations
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS mp_allocations (
                        mp_id SERIAL PRIMARY KEY,
                        sr_no VARCHAR(50),
                        state VARCHAR(100) NOT NULL,
                        mp_name VARCHAR(255) NOT NULL,
                        constituency VARCHAR(255) NOT NULL,
                        category VARCHAR(100),
                        allocated_amount_inr DOUBLE PRECISION,
                        allocated_amount_crores DOUBLE PRECISION,
                        is_baseline_14_7cr INTEGER DEFAULT 0,
                        is_missing_allocation INTEGER DEFAULT 0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        CONSTRAINT unique_state_mp_const UNIQUE(state, mp_name, constituency)
                    );
                """)

                # Table 3: Model Execution Runs
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS model_runs (
                        run_id SERIAL PRIMARY KEY,
                        model_version VARCHAR(50) NOT NULL,
                        dataset_version_tag VARCHAR(100) NOT NULL,
                        feature_version VARCHAR(50) NOT NULL,
                        algorithm VARCHAR(100) NOT NULL,
                        parameters_json TEXT NOT NULL,
                        random_seed INTEGER NOT NULL,
                        records_analyzed INTEGER NOT NULL,
                        anomalies_flagged INTEGER NOT NULL,
                        status VARCHAR(50) NOT NULL,
                        executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)

                # Table 4: Persisted Anomaly Signals
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS anomaly_signals (
                        signal_id SERIAL PRIMARY KEY,
                        run_id INTEGER NOT NULL REFERENCES model_runs(run_id) ON DELETE CASCADE,
                        mp_id VARCHAR(50) NOT NULL,
                        sr_no VARCHAR(50),
                        state VARCHAR(100) NOT NULL,
                        mp_name VARCHAR(255) NOT NULL,
                        constituency VARCHAR(255) NOT NULL,
                        allocated_amount_inr DOUBLE PRECISION,
                        allocated_amount_crores DOUBLE PRECISION,
                        risk_score DOUBLE PRECISION NOT NULL,
                        ml_anomaly_score DOUBLE PRECISION NOT NULL,
                        multi_method_agreement VARCHAR(100) NOT NULL,
                        risk_level VARCHAR(50) NOT NULL,
                        risk_color VARCHAR(50) NOT NULL,
                        signal_type VARCHAR(100) NOT NULL,
                        algorithms_triggered_json TEXT NOT NULL,
                        signal_categories_json TEXT NOT NULL,
                        evidence_breakdown_json TEXT NOT NULL,
                        disclaimer TEXT NOT NULL,
                        dataset_source VARCHAR(255) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)

                # Table 5: Investigation Audit Logs
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS investigation_audit_logs (
                        log_id SERIAL PRIMARY KEY,
                        mp_id INTEGER NOT NULL,
                        mp_name VARCHAR(255) NOT NULL,
                        status VARCHAR(100) NOT NULL,
                        nodal_officer VARCHAR(255),
                        note TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)

                # Table 6: System Users & Roles (RBAC)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users_and_roles (
                        user_id SERIAL PRIMARY KEY,
                        username VARCHAR(100) NOT NULL UNIQUE,
                        role VARCHAR(50) NOT NULL,
                        department VARCHAR(255) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)

                # Create Indexes for query performance
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_mp_allocations_state ON mp_allocations(state);")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_anomaly_signals_run_id ON anomaly_signals(run_id);")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_audit_logs_mp_id ON investigation_audit_logs(mp_id);")

                # Seed default RBAC users if table empty
                cursor.execute("SELECT COUNT(*) FROM users_and_roles;")
                count = cursor.fetchone()[0]
                if count == 0:
                    cursor.executemany("""
                        INSERT INTO users_and_roles (username, role, department)
                        VALUES (%s, %s, %s);
                    """, [
                        ("admin_mospi", "ADMIN", "Data Informatics & Innovation Division"),
                        ("nodal_officer_tg", "NODAL_OFFICER", "Telangana District Secretariat"),
                        ("nodal_officer_mh", "NODAL_OFFICER", "Maharashtra District Secretariat"),
                        ("auditor_cag", "ANALYST", "Comptroller & Auditor General Audit Wing"),
                        ("public_researcher", "VIEWER", "Public Policy Research Cell")
                    ])
            conn.commit()

        # Idempotent CSV sync
        self.sync_csv_to_db()

    def compute_csv_hash(self, csv_path: str) -> str:
        sha256 = hashlib.sha256()
        with open(csv_path, 'rb') as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()

    def sync_csv_to_db(self, csv_path: str = CSV_PATH) -> str:
        if not os.path.exists(csv_path):
            return "NO_FILE"

        csv_hash = self.compute_csv_hash(csv_path)
        version_tag = f"v2026.08-{csv_hash[:8]}"

        df = pd.read_csv(csv_path)
        df.columns = [c.replace("'", "").replace('"', '').strip() for c in df.columns]

        # Filter out Grand Total row
        gt_mask = df['Sr. No.'].astype(str).str.contains('Grand Total', case=False, na=False)
        df_mps = df[~gt_mask].copy()

        sr_col = 'Sr. No.'
        state_col = 'State'
        mp_col = [c for c in df_mps.columns if 'MP' in c or 'Member' in c or 'Hon' in c][0]
        const_col = 'Constituency'
        amt_col = [c for c in df_mps.columns if 'Allocated' in c or 'AMOUNT' in c][0]
        cat_col = [c for c in df_mps.columns if 'Category' in c]
        category_key = cat_col[0] if cat_col else None

        valid_amt = pd.to_numeric(df_mps[amt_col].astype(str).str.replace(',', '').str.strip(), errors='coerce').dropna()
        total_sum = float(valid_amt.sum())
        total_records = len(df_mps)
        valid_records = len(valid_amt)
        missing_records = total_records - valid_records

        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT version_id FROM dataset_versions WHERE version_tag = %s;", (version_tag,))
                existing_ver = cursor.fetchone()

                if not existing_ver:
                    cursor.execute("""
                        INSERT INTO dataset_versions (
                            version_tag, checksum_sha256, source_filename,
                            total_records, valid_records, missing_records, total_allocation_inr
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s);
                    """, (version_tag, csv_hash, os.path.basename(csv_path), total_records, valid_records, missing_records, total_sum))

                cursor.execute("SELECT COUNT(*) FROM mp_allocations;")
                if cursor.fetchone()[0] == 0:
                    for idx, row in df_mps.iterrows():
                        sr_no = str(row[sr_col]).strip()
                        state = str(row[state_col]).strip()
                        mp_name = str(row[mp_col]).strip()
                        constituency = str(row[const_col]).strip()
                        category = str(row[category_key]).strip() if category_key and not pd.isna(row[category_key]) else 'General'
                        
                        raw_amt = str(row[amt_col]).replace(',', '').strip()
                        amt_num = pd.to_numeric(raw_amt, errors='coerce')
                        
                        is_missing = 1 if pd.isna(amt_num) else 0
                        amt_inr = float(amt_num) if not is_missing else None
                        amt_cr = round(amt_inr / 1e7, 2) if not is_missing else None
                        is_base = 1 if (amt_inr and abs(amt_inr - 147000000.0) < 1.0) else 0

                        cursor.execute("""
                            INSERT INTO mp_allocations (
                                sr_no, state, mp_name, constituency, category,
                                allocated_amount_inr, allocated_amount_crores,
                                is_baseline_14_7cr, is_missing_allocation
                            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT (state, mp_name, constituency) DO NOTHING;
                        """, (sr_no, state, mp_name, constituency, category, amt_inr, amt_cr, is_base, is_missing))

            conn.commit()

        return version_tag

    def save_model_run_and_signals(
        self,
        model_version: str,
        dataset_version_tag: str,
        feature_version: str,
        algorithm: str,
        parameters: Dict[str, Any],
        random_seed: int,
        results: List[Dict[str, Any]]
    ) -> int:
        anomalies_count = sum(1 for r in results if r['risk_level'] in ['HIGH', 'CRITICAL'])
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO model_runs (
                        model_version, dataset_version_tag, feature_version,
                        algorithm, parameters_json, random_seed, records_analyzed,
                        anomalies_flagged, status
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING run_id;
                """, (
                    model_version, dataset_version_tag, feature_version,
                    algorithm, json.dumps(parameters, default=str), random_seed,
                    len(results), anomalies_count, "COMPLETED_AND_ACTIVE"
                ))
                run_id = cursor.fetchone()[0]

                for r in results:
                    risk_score_val = float(r['risk_score'])
                    ml_score_val = float(r['ml_anomaly_score'])
                    amt_inr_val = float(r['allocated_amount_inr']) if r['allocated_amount_inr'] is not None else None
                    amt_cr_val = float(r['allocated_amount_crores']) if r['allocated_amount_crores'] is not None else None

                    cursor.execute("""
                        INSERT INTO anomaly_signals (
                            run_id, mp_id, sr_no, state, mp_name, constituency,
                            allocated_amount_inr, allocated_amount_crores,
                            risk_score, ml_anomaly_score, multi_method_agreement,
                            risk_level, risk_color, signal_type,
                            algorithms_triggered_json, signal_categories_json,
                            evidence_breakdown_json, disclaimer, dataset_source
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                    """, (
                        run_id, str(r['mp_id']), str(r['sr_no']), str(r['state']), str(r['mp_name']), str(r['constituency']),
                        amt_inr_val, amt_cr_val,
                        risk_score_val, ml_score_val, str(r['multi_method_agreement']),
                        str(r['risk_level']), str(r['risk_color']), str(r['signal_type']),
                        json.dumps(r['algorithms_triggered'], default=str),
                        json.dumps(r['signal_categories'], default=str),
                        json.dumps(r['evidence_breakdown'], default=str),
                        str(r['disclaimer']), str(r['dataset_source'])
                    ))

            conn.commit()
            return run_id

    def get_latest_model_run_signals(self) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT * FROM model_runs ORDER BY executed_at DESC LIMIT 1;")
                run = cursor.fetchone()
                if not run:
                    return None

                cursor.execute("SELECT * FROM anomaly_signals WHERE run_id = %s ORDER BY risk_score DESC;", (run['run_id'],))
                rows = cursor.fetchall()
                
                signals = []
                for row in rows:
                    r = dict(row)
                    r['algorithms_triggered'] = json.loads(r['algorithms_triggered_json'])
                    r['signal_categories'] = json.loads(r['signal_categories_json'])
                    r['evidence_breakdown'] = json.loads(r['evidence_breakdown_json'])
                    signals.append(r)

                return {
                    "run_info": dict(run),
                    "signals": signals
                }

    def get_summary_stats(self) -> Dict[str, Any]:
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT COUNT(*) as total FROM mp_allocations;")
                total_mps = cursor.fetchone()['total']

                cursor.execute("SELECT COUNT(*) as valid FROM mp_allocations WHERE is_missing_allocation = 0;")
                valid_mps = cursor.fetchone()['valid']

                cursor.execute("SELECT SUM(allocated_amount_inr) as total_sum FROM mp_allocations WHERE is_missing_allocation = 0;")
                total_sum = cursor.fetchone()['total_sum'] or 0.0

                cursor.execute("SELECT COUNT(DISTINCT state) as states FROM mp_allocations;")
                total_states = cursor.fetchone()['states']

                cursor.execute("SELECT * FROM dataset_versions ORDER BY ingested_at DESC LIMIT 1;")
                latest_ver = cursor.fetchone()

                db_label = "Supabase Cloud PostgreSQL (Active Production Database)" if PG_HOST not in ["localhost", "127.0.0.1"] else "PostgreSQL 15 (Local Production Engine)"

                return {
                    "db_type": db_label,
                    "db_status": "ONLINE & CONNECTED",
                    "database_url_masked": f"postgresql://{PG_USER}:***@{PG_HOST}:{PG_PORT}/{PG_DBNAME}",
                    "total_mp_records": total_mps,
                    "valid_records": valid_mps,
                    "missing_records": total_mps - valid_mps,
                    "total_allocation_inr": float(total_sum),
                    "total_allocation_crores": round(float(total_sum) / 1e7, 2),
                    "unique_states": total_states,
                    "latest_dataset_version": dict(latest_ver) if latest_ver else None
                }

    def add_audit_log(self, mp_id: int, mp_name: str, status: str, note: Optional[str] = None, officer: Optional[str] = None):
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO investigation_audit_logs (mp_id, mp_name, status, note, nodal_officer)
                    VALUES (%s, %s, %s, %s, %s);
                """, (mp_id, mp_name, status, note, officer))
            conn.commit()

    def get_audit_logs(self, mp_id: Optional[int] = None) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                if mp_id:
                    cursor.execute("SELECT * FROM investigation_audit_logs WHERE mp_id = %s ORDER BY created_at DESC;", (mp_id,))
                else:
                    cursor.execute("SELECT * FROM investigation_audit_logs ORDER BY created_at DESC LIMIT 100;")
                return [dict(row) for row in cursor.fetchall()]

db_service = MPLADSDatabase()
