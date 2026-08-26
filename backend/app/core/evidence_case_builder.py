from typing import Dict, List, Any, Optional
from datetime import datetime, timezone
from app.schemas.layer2_schema import (
    GovernanceInvestigationCase,
    GovernanceInvestigationStatus,
    EvidenceFactor,
    SignalDetail
)
from app.ml.work_irregularity_engine import work_irregularity_engine

class EvidenceCaseBuilder:
    """
    Governance Evidence Case Builder.
    Aggregates Layer 1 Allocation Anomalies + Layer 2 Work-Level Irregularities
    into a traceable, explainable, governance-safe Investigation Case.
    
    STRICT GOVERNANCE RULES:
    1. NEVER assigns 'FRAUD_CONFIRMED' or 'GUILTY' status.
    2. Default investigation status is 'REVIEW_REQUIRED'.
    3. Allowed statuses ONLY:
       - REVIEW_REQUIRED
       - UNDER_INVESTIGATION
       - EVIDENCE_PENDING
       - CLEARED
       - REFERRED_FOR_FURTHER_REVIEW
    4. Separates verified FACTS from ML SIGNALS and EVIDENCE.
    5. Explicitly lists MISSING EVIDENCE.
    """
    
    # Store in-memory status updates for human officers
    _officer_status_store: Dict[str, Dict[str, Any]] = {}

    @classmethod
    def update_officer_status(cls, case_id: str, new_status: GovernanceInvestigationStatus, officer_username: str) -> Dict[str, Any]:
        if new_status not in GovernanceInvestigationStatus:
            raise ValueError(f"Invalid status '{new_status}'. Allowed statuses: {[s.value for s in GovernanceInvestigationStatus]}")
            
        timestamp = datetime.now(timezone.utc).isoformat()
        cls._officer_status_store[case_id] = {
            "investigation_status": new_status,
            "status_updated_by": officer_username,
            "status_updated_at": timestamp
        }
        return cls._officer_status_store[case_id]

    def build_case(self, layer1_result: Dict[str, Any], work_records: Optional[List[Dict[str, Any]]] = None) -> GovernanceInvestigationCase:
        mp_id = layer1_result.get("mp_id", "MP_UNKNOWN")
        case_id = f"CASE_{mp_id}"
        
        # 1. Facts Extraction (Raw Official Values Only)
        amt_inr = layer1_result.get("allocated_amount_inr")
        amt_cr = layer1_result.get("allocated_amount_crores")
        facts = {
            "mp_id": mp_id,
            "sr_no": layer1_result.get("sr_no"),
            "mp_name": layer1_result.get("mp_name"),
            "state": layer1_result.get("state"),
            "constituency": layer1_result.get("constituency"),
            "allocated_amount_inr": amt_inr,
            "allocated_amount_crores": amt_cr,
            "official_baseline_inr": 147000000.0,
            "official_dataset_source": layer1_result.get("dataset_source", "Allocated Limit for Honble MPs.csv")
        }

        # 2. ML Signals Aggregation
        ml_signals: List[SignalDetail] = []
        for cat in layer1_result.get("signal_categories", []):
            ml_signals.append(SignalDetail(
                signal=cat.get("signal", "ALLOCATION_SIGNAL"),
                value=cat.get("value", "N/A"),
                severity=cat.get("severity", "MEDIUM"),
                source=cat.get("source", "scikit_learn_anomaly_pipeline"),
                method="Layer 1 Allocation Anomaly Model"
            ))

        # 3. Layer 1 Evidence Factors
        evidence: List[EvidenceFactor] = []
        for ev in layer1_result.get("evidence_breakdown", []):
            evidence.append(EvidenceFactor(
                factor=ev.get("factor", "Allocation Metric"),
                impact=ev.get("impact", "0 pts"),
                description=ev.get("description", ""),
                source_ref="Layer 1: Official Allocation Limit Dataset"
            ))

        # 4. Evaluate Layer 2 Work-Level Irregularity Engine
        layer2_eval = work_irregularity_engine.evaluate_works(work_records or [])
        
        if layer2_eval.get("is_layer2_active"):
            for sig in layer2_eval.get("layer2_signals_triggered", []):
                ml_signals.append(SignalDetail(
                    signal=sig.get("signal"),
                    value=sig.get("value"),
                    severity=sig.get("severity"),
                    source=sig.get("source"),
                    method=sig.get("method")
                ))
            for ev in layer2_eval.get("layer2_evidence", []):
                evidence.append(EvidenceFactor(
                    factor=ev.get("factor"),
                    impact=ev.get("impact"),
                    description=ev.get("description"),
                    source_ref=ev.get("source_ref", "Layer 2: eSAKSHI Work Ledger")
                ))

        # 5. Missing Evidence Assembly
        missing_evidence: List[str] = []
        if amt_inr is None:
            missing_evidence.append("Allocation limit record in official MoSPI CSV dataset")
            
        missing_evidence.extend(layer2_eval.get("layer2_missing_evidence", []))

        # 6. Combined Evidence-Based Risk Score (0-100)
        base_l1_score = float(layer1_result.get("risk_score", 0.0))
        l2_delta = float(layer2_eval.get("layer2_risk_score_delta", 0.0))
        final_score = min(100.0, base_l1_score + l2_delta)

        # Risk Level Tier
        if final_score >= 81.0:
            risk_level = "CRITICAL"
        elif final_score >= 61.0:
            risk_level = "HIGH"
        elif final_score >= 31.0:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        # 7. Governance Status Check (Human Override or Default)
        stored_override = self._officer_status_store.get(case_id)
        if stored_override:
            current_status = stored_override["investigation_status"]
            updated_by = stored_override["status_updated_by"]
            updated_at = stored_override["status_updated_at"]
        else:
            current_status = GovernanceInvestigationStatus.REVIEW_REQUIRED
            updated_by = "SYSTEM_INITIALIZED"
            updated_at = datetime.now(timezone.utc).isoformat()

        return GovernanceInvestigationCase(
            case_id=case_id,
            mp_id=mp_id,
            mp_name=layer1_result.get("mp_name", ""),
            state=layer1_result.get("state", ""),
            constituency=layer1_result.get("constituency", ""),
            allocated_amount=amt_inr,
            risk_score=round(final_score, 1),
            risk_level=risk_level,
            facts=facts,
            ml_signals=ml_signals,
            evidence=evidence,
            missing_evidence=missing_evidence,
            investigation_status=current_status,
            status_updated_by=updated_by,
            status_updated_at=updated_at
        )

# Singleton instance
evidence_case_builder = EvidenceCaseBuilder()
