from typing import Optional, List, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field

class GovernanceInvestigationStatus(str, Enum):
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    UNDER_INVESTIGATION = "UNDER_INVESTIGATION"
    EVIDENCE_PENDING = "EVIDENCE_PENDING"
    CLEARED = "CLEARED"
    REFERRED_FOR_FURTHER_REVIEW = "REFERRED_FOR_FURTHER_REVIEW"

class WorkLevelRecord(BaseModel):
    """
    Schema for optional work-level eSAKSHI project dataset.
    All fields are optional to handle datasets where work-level data is unavailable.
    """
    work_id: Optional[str] = None
    mp_id: Optional[str] = None
    state: Optional[str] = None
    constituency: Optional[str] = None
    work_type: Optional[str] = None
    sanction_date: Optional[str] = None
    estimated_cost: Optional[float] = None
    sanctioned_amount: Optional[float] = None
    expenditure: Optional[float] = None
    bill_id: Optional[str] = None
    bill_amount: Optional[float] = None
    payment_amount: Optional[float] = None
    payment_date: Optional[str] = None
    vendor_id: Optional[str] = None
    vendor_name: Optional[str] = None
    physical_progress_pct: Optional[float] = None
    completion_status: Optional[str] = None
    completion_date: Optional[str] = None
    document_ids: Optional[List[str]] = Field(default_factory=list)
    photo_metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

class EvidenceFactor(BaseModel):
    factor: str
    impact: str
    description: str
    source_ref: Optional[str] = None

class SignalDetail(BaseModel):
    signal: str
    value: Any
    severity: str
    source: str
    method: str

class GovernanceInvestigationCase(BaseModel):
    case_id: str
    mp_id: str
    mp_name: str
    state: str
    constituency: str
    allocated_amount: Optional[float] = None
    risk_score: float
    risk_level: str
    facts: Dict[str, Any]
    ml_signals: List[SignalDetail]
    evidence: List[EvidenceFactor]
    missing_evidence: List[str]
    investigation_status: GovernanceInvestigationStatus
    status_updated_by: Optional[str] = "SYSTEM_INITIALIZED"
    status_updated_at: Optional[str] = None
