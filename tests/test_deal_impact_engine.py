from src.deal_impact_engine import map_deal_impact, diligence_question

def test_critical_erp_mapping():
    row={"title":"Unsupported critical ERP","cyber_domain":"Infrastructure Security","risk_rating":"Critical","pre_close_relevance":True,"day_1_relevance":False,"integration_relevance":True,"remediation_time_months":12,"remediation_complexity":"High"}
    impacts=map_deal_impact(row)
    assert "Specialist escalation pending evidence" in impacts
    assert "Integration planning dependency" in impacts
    assert "vendor security support" in diligence_question(row)
    assert "revenue-generating" in diligence_question(row)
    assert not any("Deal-breaker" in impact or "Purchase-price" in impact for impact in impacts)

def test_day_one_mapping():
    row={"title":"MFA gap","cyber_domain":"Identity","risk_rating":"High","pre_close_relevance":False,"day_1_relevance":True,"integration_relevance":False,"remediation_time_months":2,"remediation_complexity":"Medium"}
    assert "Day 1 safeguard / readiness planning" in map_deal_impact(row)

def test_identity_and_incident_questions_request_specific_evidence():
    identity=diligence_question({"title":"MFA gap","cyber_domain":"Identity & Access Management"})
    incident=diligence_question({"title":"Vendor incident evidence remains incomplete","cyber_domain":"Third-Party Risk"})
    assert "percentage and number" in identity and "bypass MFA" in identity
    assert "chronology" in incident and "insurance" in incident and "uncorroborated" in incident
