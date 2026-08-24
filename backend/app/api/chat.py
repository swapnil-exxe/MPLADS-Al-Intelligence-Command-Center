from fastapi import APIRouter
from pydantic import BaseModel
from app.services.ai_investigator import ai_investigator

router = APIRouter(prefix="/api/ai", tags=["AI Investigator"])

class InvestigateRequest(BaseModel):
    query: str

@router.post("/investigate")
def investigate_query(req: InvestigateRequest):
    """
    Grounded AI Investigator query endpoint.
    Answers strictly using real MoSPI dataset metrics or returns explicit scope boundaries.
    """
    return ai_investigator.answer_query(req.query)
