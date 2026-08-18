from src.deal_impact_engine import map_deal_impact, diligence_question

def test_critical_erp_mapping():
    row={"title":"Unsupported critical ERP","cyber_domain":"Infrastructure Security","risk_rating":"Critical","pre_close_relevance":True,"day_1_relevance":False,"integration_relevance":True,"remediation_time_months":12,"remediation_complexity":"High"}
    impacts=map_deal_impact(row)
    assert "Purchase-price consideration" in impacts
    assert "Integration dependency" in impacts
    assert "funded replacement plan" in diligence_question(row)

def test_day_one_mapping():
    row={"title":"MFA gap","cyber_domain":"Identity","risk_rating":"High","pre_close_relevance":False,"day_1_relevance":True,"integration_relevance":False,"remediation_time_months":2,"remediation_complexity":"Medium"}
    assert "Day-1 requirement" in map_deal_impact(row)
