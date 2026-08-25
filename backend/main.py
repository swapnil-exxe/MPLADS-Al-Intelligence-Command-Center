import os
import datetime
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from apscheduler.schedulers.background import BackgroundScheduler

from app.api import analytics, risk, chat, demo, system, auth, exports
from app.schemas.schemas import HealthCheckResponse
from app.db.database import db_service
from app.services.real_data_service import real_data_service
from ml.anomaly_detector import anomaly_detector

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("mplads_backend")

# APScheduler for automatic periodic ML re-evaluation
scheduler = BackgroundScheduler(daemon=True)

def scheduled_ml_reevaluation():
    """
    Periodic background job re-evaluating ML models and persisting signals to Supabase.
    """
    try:
        logger.info("Executing scheduled periodic ML model re-evaluation...")
        df = real_data_service.get_all_mps_df()
        anomalies = anomaly_detector.fit_and_predict(df, force_refit=True)
        high_risk_count = len([a for a in anomalies if a['risk_level'] in ['HIGH', 'CRITICAL']])
        
        db_service.save_model_run_and_signals(
            model_version="v2.0-isolation-forest-iqr",
            dataset_version_tag="v2026.08-1ad9c80d",
            feature_version="f_v2",
            algorithm="IsolationForest(n_estimators=300, seed=42) + Tukey IQR + Z-Score",
            parameters={"n_estimators": 300, "contamination": 0.08, "random_state": 42},
            random_seed=42,
            results=anomalies
        )
        logger.info(f"Scheduled ML re-evaluation complete. Flagged {high_risk_count} anomalies.")
    except Exception as e:
        logger.error(f"Error in scheduled ML re-evaluation: {str(e)}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # App startup: Start background scheduler
    logger.info("Starting background APScheduler for automatic ML re-evaluation...")
    try:
        scheduler.add_job(scheduled_ml_reevaluation, 'interval', hours=6, id='scheduled_ml_reevaluation', replace_existing=True)
        scheduler.start()
    except Exception as e:
        logger.warning(f"Scheduler initialization warning: {str(e)}")
    yield
    # App shutdown
    logger.info("Shutting down APScheduler...")
    if scheduler.running:
        scheduler.shutdown()

app = FastAPI(
    title="MPLADS AI Intelligence Command Center API — SIH26102",
    description="Official FastAPI Backend for MoSPI MPLADS AI Monitoring, Risk Scoring & Anomaly Intelligence",
    version="2.0.0",
    lifespan=lifespan
)

# CORS configuration (Production hardening: Specific Origins)
allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "")
if allowed_origins_env:
    allowed_origins = [orig.strip() for orig in allowed_origins_env.split(",") if orig.strip()]
else:
    allowed_origins = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8001"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Production Security Headers Middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response

# Safe Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception on {request.url.path}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal server error occurred. Please contact the system administrator."}
    )

# Routers
app.include_router(auth.router)
app.include_router(exports.router)
app.include_router(analytics.router)
app.include_router(risk.router)
app.include_router(chat.router)
app.include_router(demo.router)
app.include_router(system.router)

@app.get("/", tags=["Health & Root"])
def root():
    return {
        "status": "online",
        "system": "MPLADS AI Intelligence Command Center API",
        "version": "2.0.0",
        "dataset": "Official MoSPI Allocated Limit for Honble MPs.csv",
        "docs": "/docs"
    }

@app.get("/health", response_model=HealthCheckResponse, tags=["Health & Root"])
@app.get("/api/system/health", response_model=HealthCheckResponse, tags=["Health & Root"])
def health_check():
    db_stats = db_service.get_summary_stats()
    return HealthCheckResponse(
        status="healthy",
        api="operational",
        database=f"connected ({db_stats['total_mp_records']} MP records ingested)",
        dataset="verified_and_synced",
        ml_engine="fitted_and_reproducible",
        timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
