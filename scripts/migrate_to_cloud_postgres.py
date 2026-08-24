import os
import sys
import psycopg2
from psycopg2.extras import RealDictCursor, execute_values

LOCAL_DB_URI = os.getenv("LOCAL_DATABASE_URL", "postgresql://swapnil@localhost:5432/mplads_db")

def migrate_to_cloud(cloud_db_uri: str):
    print("==================================================")
    print("MPLADS COMMAND CENTER: CLOUD POSTGRESQL MIGRATION")
    print("==================================================")
    print(f"Reading from Local PostgreSQL: {LOCAL_DB_URI}")
    print("Connecting to Supabase Cloud PostgreSQL...")

    local_conn = psycopg2.connect(LOCAL_DB_URI)
    cloud_conn = psycopg2.connect(cloud_db_uri, sslmode="require")

    local_cur = local_conn.cursor(cursor_factory=RealDictCursor)
    cloud_cur = cloud_conn.cursor()

    # Step 1: Ensure Target Cloud Schema
    print("\n--- STEP 1: INITIALIZING TARGET CLOUD SCHEMAS ---")
    cloud_cur.execute("""
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
        CREATE TABLE IF NOT EXISTS investigation_audit_logs (
            log_id SERIAL PRIMARY KEY,
            mp_id INTEGER NOT NULL,
            mp_name VARCHAR(255) NOT NULL,
            status VARCHAR(100) NOT NULL,
            nodal_officer VARCHAR(255),
            note TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS users_and_roles (
            user_id SERIAL PRIMARY KEY,
            username VARCHAR(100) NOT NULL UNIQUE,
            role VARCHAR(50) NOT NULL,
            department VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    cloud_conn.commit()

    # Step 2: Migrate Records Table by Table using execute_values
    tables = [
        "dataset_versions",
        "mp_allocations",
        "model_runs",
        "anomaly_signals",
        "investigation_audit_logs",
        "users_and_roles"
    ]

    print("\n--- STEP 2: MIGRATING TABLES & RECORDS ---")
    for t in tables:
        local_cur.execute(f"SELECT * FROM {t};")
        rows = local_cur.fetchall()
        print(f"Migrating table [{t}]: {len(rows)} records...")

        if not rows:
            continue

        cols = list(rows[0].keys())
        cols_str = ", ".join(cols)

        tuples = [tuple(r[c] for c in cols) for r in rows]
        
        query = f"INSERT INTO {t} ({cols_str}) VALUES %s ON CONFLICT DO NOTHING;"
        execute_values(cloud_cur, query, tuples)
        cloud_conn.commit()

    # Step 3: Verification
    print("\n--- STEP 3: VERIFYING MIGRATED CLOUD RECORD COUNTS ---")
    for t in tables:
        cloud_cur.execute(f"SELECT COUNT(*) FROM {t};")
        cnt = cloud_cur.fetchone()[0]
        print(f"Supabase Cloud PostgreSQL table [{t}]: {cnt} records")

    local_conn.close()
    cloud_conn.close()
    print("\n✓ SUPABASE CLOUD POSTGRESQL MIGRATION SUCCESSFUL!")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cloud_uri = sys.argv[1]
    else:
        cloud_uri = os.getenv("CLOUD_DATABASE_URL", "")

    if not cloud_uri:
        print("Usage: python scripts/migrate_to_cloud_postgres.py <CLOUD_POSTGRESQL_CONNECTION_STRING>")
        sys.exit(1)

    migrate_to_cloud(cloud_uri)
