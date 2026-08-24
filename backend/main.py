import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import analytics, risk, chat, demo, system
from app.schemas.schemas import HealthCheckResponse
from app.db.database import db_service

app = FastAPI(
    title="MPLADS AI Intelligence Command Center API — SIH26102",
    description="Official FastAPI Backend for MoSPI MPLADS AI Monitoring, Risk Scoring & Anomaly Intelligence",
    version="2.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
