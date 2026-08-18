import pandas as pd
from src.remediation_engine import portfolio_totals, add_remediation_analysis

def test_totals_and_order():
    df=pd.DataFrame({"estimated_low_cost":[1,2],"estimated_base_cost":[2,3],"estimated_high_cost":[4,5]})
    assert portfolio_totals(df)=={"Low":3.0,"Base":5.0,"High":9.0}

def test_timing_rule():
    df=pd.DataFrame([{"pre_close_relevance":True,"day_1_relevance":False,"risk_rating":"Critical","remediation_time_months":12}])
    assert add_remediation_analysis(df).iloc[0].roadmap_period=="Pre-close"
