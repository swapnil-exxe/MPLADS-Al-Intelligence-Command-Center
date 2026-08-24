from fastapi import APIRouter, Query
from typing import Optional
from app.services.demo_data_service import demo_data_service, DISCLOSURE_LABEL

router = APIRouter(prefix="/api/demo", tags=["Demo Simulation (Isolated)"])

@router.get("/projects")
def get_demo_projects(
    category: Optional[str] = Query(None),
    risk_level: Optional[str] = Query(None)
):
    """
    Isolated endpoint returning simulated micro-project data for UI demonstration.
    STRICT COMPLIANCE: Includes explicit demo disclosure label on every response.
    """
    projects = demo_data_service.get_demo_projects(category=category, risk_level=risk_level)
    return {
        "disclosure_notice": DISCLOSURE_LABEL,
        "is_demo_simulation": True,
        "count": len(projects),
        "projects": projects
    }

@router.get("/fraud-graph")
def get_demo_fraud_graph():
    """Returns entity relationship graph for demo fraud intelligence view."""
    return demo_data_service.get_demo_fraud_graph()
