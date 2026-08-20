from src.risk_engine import score_finding

def finding(**changes):
    row={"severity":"Low","likelihood":"Low","business_criticality":"Low","remediation_complexity":"Low","affected_assets":1}; row.update(changes); return row

def test_rules_classify_known_extremes():
    assert score_finding(finding())[0]=="Low"
    assert score_finding(finding(severity="Critical",likelihood="High",business_criticality="Critical",remediation_complexity="High",affected_assets=20))[0]=="Critical"

def test_explanation_is_transparent():
    rating,score,text=score_finding(finding(severity="High",likelihood="High",business_criticality="High",remediation_complexity="Medium",affected_assets=6))
    assert rating=="High" and str(score) in text and "reported breadth" in text and "not a residual-risk conclusion" in text

def test_remediation_complexity_does_not_inflate_exposure():
    low=score_finding(finding(remediation_complexity="Low"))[:2]
    high=score_finding(finding(remediation_complexity="High"))[:2]
    assert low==high
