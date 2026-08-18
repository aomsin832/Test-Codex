import pandas as pd
from src.remediation_engine import (add_remediation_analysis, build_integration_roadmap,
                                    build_roadmap, full_delivery_horizon, portfolio_totals)

def test_totals_and_order():
    df=pd.DataFrame({"estimated_low_cost":[1,2],"estimated_base_cost":[2,3],"estimated_high_cost":[4,5]})
    assert portfolio_totals(df)=={"Low":3.0,"Base":5.0,"High":9.0}

def test_timing_rule():
    df=pd.DataFrame([{"pre_close_relevance":True,"day_1_relevance":False,"risk_rating":"Critical","remediation_time_months":12}])
    assert add_remediation_analysis(df).iloc[0].roadmap_period=="Pre-close"

def test_pre_close_is_a_diligence_action_not_a_remediation_promise():
    df=pd.DataFrame([{"finding_id":"F1","title":"Example","cyber_domain":"Identity","pre_close_relevance":True,"day_1_relevance":True,"risk_rating":"High","remediation_time_months":9,"estimated_base_cost":10,"remediation_complexity":"High","deal_rationale":"Validate."}])
    enriched=add_remediation_analysis(df)
    assert enriched.iloc[0].remediation_category=="Pre-close diligence / deal treatment"
    roadmap=build_roadmap(enriched)
    assert roadmap.iloc[0]["Action"].startswith("Validate evidence")
    assert roadmap.iloc[0]["Estimated delivery months"]==9

def test_full_delivery_horizon_is_separate_from_transaction_timing():
    assert full_delivery_horizon(1)=="Day 30"
    assert full_delivery_horizon(4)=="Day 100"
    assert full_delivery_horizon(12)=="6–12 months"
    assert full_delivery_horizon(18)=="Longer-term transformation"

def test_integration_roadmap_retains_pre_close_day_one_and_delivery_actions():
    df=pd.DataFrame([{"finding_id":"F1","title":"Example","cyber_domain":"Infrastructure Security","pre_close_relevance":True,"day_1_relevance":True,"risk_rating":"High","remediation_time_months":18,"estimated_base_cost":100,"remediation_complexity":"High","deal_rationale":"Validate."}])
    roadmap=build_integration_roadmap(add_remediation_analysis(df))
    assert roadmap.Stage.tolist()==["Pre-close","Day 1","Longer-term transformation"]
    assert roadmap["Base cost reference"].eq(100).all()
