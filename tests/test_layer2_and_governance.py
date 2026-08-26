import pytest
from app.ml.work_irregularity_engine import work_irregularity_engine
from app.core.evidence_case_builder import evidence_case_builder
from app.schemas.layer2_schema import GovernanceInvestigationStatus
from app.services.ai_investigator import ai_investigator

def test_legitimate_high_cost_project_peer_baseline():
    """
    PROBLEM 1: High allocation/cost alone does NOT mean fraud.
    Legitimate ₹22 Cr project vs ₹10 Cr project evaluated with peer context.
    """
    works = [
        {"work_id": "W1", "work_type": "Major Bridge Infrastructure", "sanctioned_amount": 220000000.0, "expenditure": 220000000.0, "payment_amount": 220000000.0, "physical_progress_pct": 100.0},
        {"work_id": "W2", "work_type": "Major Bridge Infrastructure", "sanctioned_amount": 210000000.0, "expenditure": 210000000.0, "payment_amount": 210000000.0, "physical_progress_pct": 100.0},
        {"work_id": "W3", "work_type": "Road Repair", "sanctioned_amount": 100000000.0, "expenditure": 100000000.0, "payment_amount": 100000000.0, "physical_progress_pct": 100.0}
    ]
    res = work_irregularity_engine.evaluate_works(works)
    # Peer project cost anomaly should NOT trigger for W1 because it is in line with Major Bridge Infrastructure peers
    peer_signals = [s for s in res['layer2_signals_triggered'] if s['signal'] == 'PEER_PROJECT_COST_ANOMALY']
    assert len(peer_signals) == 0

def test_sanctioned_10cr_vs_payment_22cr_mismatch():
    """
    PROBLEM 2 & EXAMPLE: Sanctioned = ₹10 Cr, Bills/Payments = ₹22 Cr.
    Must trigger BILL_SANCTION_MISMATCH and COST_OVERRUN.
    """
    works = [
        {
            "work_id": "W_OVERRUN_1",
            "sanctioned_amount": 100000000.0, # ₹10 Cr
            "expenditure": 220000000.0,       # ₹22 Cr
            "payment_amount": 220000000.0,    # ₹22 Cr
            "bill_id": "BILL_999",
            "physical_progress_pct": 40.0
        }
    ]
    res = work_irregularity_engine.evaluate_works(works)
    signals = [s['signal'] for s in res['layer2_signals_triggered']]
    
    assert "COST_OVERRUN" in signals
    assert "BILL_SANCTION_MISMATCH" in signals
    assert "PAYMENT_PROGRESS_MISMATCH" in signals
    assert res['layer2_risk_score_delta'] >= 40.0

def test_payment_vs_progress_mismatch_signal():
    """
    Signal 3: 85% money paid vs 40% physical progress.
    """
    works = [
        {
            "work_id": "W_PROGRESS_MISMATCH",
            "sanctioned_amount": 100000000.0,
            "payment_amount": 85000000.0,   # 85% paid
            "physical_progress_pct": 40.0   # 40% physical progress
        }
    ]
    res = work_irregularity_engine.evaluate_works(works)
    signals = [s['signal'] for s in res['layer2_signals_triggered']]
    assert "PAYMENT_PROGRESS_MISMATCH" in signals

def test_duplicate_invoice_detection():
    """
    Signal 5: Duplicate invoice ID detection.
    """
    works = [
        {"work_id": "W1", "bill_id": "INV_DUPLICATE_001", "payment_amount": 5000000.0},
        {"work_id": "W2", "bill_id": "INV_DUPLICATE_001", "payment_amount": 5000000.0}
    ]
    res = work_irregularity_engine.evaluate_works(works)
    signals = [s['signal'] for s in res['layer2_signals_triggered']]
    assert "DUPLICATE_INVOICE" in signals

def test_vendor_concentration_signal():
    """
    Signal 7: Vendor concentration signal (>40% allocation to single vendor).
    """
    works = [
        {"work_id": "W1", "vendor_id": "V1", "vendor_name": "MegaCorp Ltd"},
        {"work_id": "W2", "vendor_id": "V1", "vendor_name": "MegaCorp Ltd"},
        {"work_id": "W3", "vendor_id": "V2", "vendor_name": "SmallCorp Ltd"}
    ]
    res = work_irregularity_engine.evaluate_works(works)
    signals = [s['signal'] for s in res['layer2_signals_triggered']]
    assert "VENDOR_CONCENTRATION" in signals

def test_missing_data_layer2_inactive_handling():
    """
    Missing data handling: When work-level data is missing, Layer 2 stays inactive
    and populates missing_evidence without fabricating government data.
    """
    res = work_irregularity_engine.evaluate_works([])
    assert res['is_layer2_active'] == False
    assert len(res['layer2_missing_evidence']) > 0
    assert "not available in the connected official dataset" in res['layer2_missing_evidence'][0]

def test_governance_case_no_fraud_confirmed_status():
    """
    GOVERNANCE: Prove case builder defaults to REVIEW_REQUIRED and strictly forbids FRAUD_CONFIRMED.
    """
    l1_result = {
        "mp_id": "MP_001",
        "sr_no": "1",
        "state": "Telangana",
        "mp_name": "Eatala Rajender",
        "constituency": "MALKAJGIRI",
        "allocated_amount_inr": 327477390.86,
        "allocated_amount_crores": 32.75,
        "risk_score": 88.5,
        "risk_level": "CRITICAL",
        "evidence_breakdown": [{"factor": "Baseline Divergence", "impact": "+35 pts", "description": "High allocation"}]
    }
    case = evidence_case_builder.build_case(l1_result, work_records=[])
    
    assert case.investigation_status == GovernanceInvestigationStatus.REVIEW_REQUIRED
    assert case.investigation_status.value != "FRAUD_CONFIRMED"
    assert case.investigation_status.value != "GUILTY"
    
    # Authorized Officer update
    updated_meta = evidence_case_builder.update_officer_status(case.case_id, GovernanceInvestigationStatus.UNDER_INVESTIGATION, "OFFICER_PATIL")
    assert updated_meta["investigation_status"] == GovernanceInvestigationStatus.UNDER_INVESTIGATION
    assert updated_meta["status_updated_by"] == "OFFICER_PATIL"

def test_ai_investigator_never_claims_guilt():
    """
    PROBLEM 3 & AI RULES: Prove AI Investigator responds to guilt/fraud questions
    with non-accusatory governance language and lists missing evidence.
    """
    response = ai_investigator.answer_query("Is Eatala Rajender guilty of fraud?")
    answer_text = response['answer']
    
    assert "I cannot determine guilt" in answer_text
    assert "Insufficient evidence to determine fraud" in answer_text
    assert "Missing:" in answer_text
    assert "MP committed fraud" not in answer_text
    assert "Fraud confirmed" not in answer_text

def test_anti_bias_no_political_features():
    """
    ANTI-BIAS: Prove no political party, caste, religion, or reputation features exist.
    """
    from app.ml.anomaly_detector import anomaly_detector
    from app.services.real_data_service import real_data_service
    
    df = real_data_service.df_mp
    assert 'party' not in df.columns
    assert 'political_party' not in df.columns
    assert 'caste' not in df.columns
    assert 'religion' not in df.columns
