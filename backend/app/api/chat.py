from fastapi import APIRouter, Request
from pydantic import BaseModel, Field
from app.services.ai_investigator import ai_investigator
from app.core.rate_limiter import limiter

router = APIRouter(prefix="/api/ai", tags=["AI Investigator"])

class InvestigateRequest(BaseModel):
    query: str = Field(..., min_length=2, max_length=1000)

@router.post("/investigate")
def investigate_query(req: InvestigateRequest, request: Request):
    """
    Grounded AI Investigator query endpoint.
    Answers strictly using real MoSPI dataset metrics or returns explicit scope boundaries.
    Rate limited to 30 requests per minute per IP.
    """
    limiter.check_rate_limit(request, endpoint_type="ai_investigate", max_requests=30, window_seconds=60)
    return ai_investigator.answer_query(req.query)
