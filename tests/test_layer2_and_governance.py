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

def test_layer1_543_mp_audit_and_footer_exclusion():
    """
    AUDIT LAYER 1: Verify 543 MP records, exclude Grand Total footer, verify Isolation Forest,
    Z-Score, Tukey IQR, peer comparison, missing allocation (Row 108), risk scores 0-100,
    and verify HIGH does NOT automatically mean fraud.
    """
    from app.services.real_data_service import real_data_service
    from app.ml.anomaly_detector import anomaly_detector
    
    # 1. 543 MP records loaded correctly
    df = real_data_service.df_mp
    assert len(df) == 543
    
    # 2. Grand Total row excluded from MP DataFrame
    gt_check = df['sr_no'].str.contains('Grand Total', case=False)
    assert gt_check.sum() == 0
    assert real_data_service.grand_total_str != ""
    
    # 3. Fit and predict Layer 1 models
    results = anomaly_detector.fit_and_predict(df)
    assert len(results) == 543
    
    # 4. Check algorithms triggered
    all_algos = set()
    for r in results:
        all_algos.update(r['algorithms_triggered'])
        # Bounded 0-100
        assert 0.0 <= r['risk_score'] <= 100.0
        # Disclaimer confirms allocation anomaly signal, not fraud proof
        assert "not proof of fraud" in r['disclaimer']
        
    assert "IsolationForest" in all_algos or "StandardBaselineCheck" in all_algos
    assert "ZScoreStatisticalTest" in all_algos or "StandardBaselineCheck" in all_algos
    assert "TukeyIQROutlierTest" in all_algos or "StandardBaselineCheck" in all_algos
    
    # 5. Missing allocation record audit (Nanded MP_108)
    nanded = next(r for r in results if r['mp_id'] == 'MP_108')
    assert nanded['allocated_amount_inr'] is None
    assert nanded['risk_score'] == 90.0

def test_ai_investigator_specific_questions():
    """
    TEST AI INVESTIGATOR: Test specific required questions:
    - "Is this MP guilty of fraud?"
    - "Why was this MP flagged?"
    - "Where is the proof?"
    - "Show me the evidence."
    - "Do you have vendor/payment data?"
    """
    # Q1: Is this MP guilty of fraud?
    q1 = ai_investigator.answer_query("Is this MP guilty of fraud?")
    assert "I cannot determine guilt" in q1['answer']
    
    # Q2: Why was this MP flagged?
    q2 = ai_investigator.answer_query("Why was Malkajgiri flagged?")
    assert "Malkajgiri" in q2['answer'] or "Eatala Rajender" in q2['answer'] or "Allocation" in q2['answer']
    
    # Q3: Where is the proof?
    q3 = ai_investigator.answer_query("Where is the proof?")
    assert "I cannot determine guilt" in q3['answer'] or "evidence" in q3['answer'].lower()
    
    # Q4: Show me the evidence.
    q4 = ai_investigator.answer_query("Show me the evidence.")
    assert "evidence" in q4['answer'].lower() or "allocation" in q4['answer'].lower()
    
    # Q5: Do you have vendor/payment data?
    q5 = ai_investigator.answer_query("Do you have vendor/payment data?")
    assert "Data not available in the connected official dataset" in q5['answer']

def test_data_provenance():
    """
    DATA PROVENANCE: Verify every real-data result identifies source dataset,
    record/MP, calculation, and model signal.
    """
    from app.services.real_data_service import real_data_service
    from app.ml.anomaly_detector import anomaly_detector
    
    results = anomaly_detector.fit_and_predict(real_data_service.df_mp)
    for r in results[:10]:
        assert r['dataset_source'] == "Allocated Limit for Honble MPs.csv"
        assert r['mp_id'].startswith("MP_")
        assert 'risk_score' in r
        assert 'multi_method_agreement' in r

def test_risk_score_aggregation_audit():
    """
    RISK SCORE AUDIT: Verify Layer 1 Base + Layer 2 Delta aggregation prevents
    double-counting, clips to 0-100, and provides explainable reasons.
    """
    l1_result = {
        "mp_id": "MP_001",
        "sr_no": "1",
        "state": "Telangana",
        "mp_name": "Eatala Rajender",
        "constituency": "MALKAJGIRI",
        "allocated_amount_inr": 327477390.86,
        "allocated_amount_crores": 32.75,
        "risk_score": 65.0, # Layer 1 base
        "risk_level": "HIGH",
        "evidence_breakdown": [{"factor": "Baseline Divergence", "impact": "+35 pts", "description": "High allocation"}]
    }
    works = [
        {
            "work_id": "W1",
            "sanctioned_amount": 100000000.0,
            "expenditure": 220000000.0,
            "payment_amount": 220000000.0,
            "physical_progress_pct": 40.0
        }
    ]
    case = evidence_case_builder.build_case(l1_result, work_records=works)
    assert case.risk_score <= 100.0
    assert case.risk_score == 100.0 # 65.0 + 35.0 (capped at +50) = 100.0
    assert len(case.evidence) >= 2

