import pandas as pd
from src.data_validation import validate_company, validate_findings, REQUIRED

def valid_frame():
    row={c:"x" for c in REQUIRED}; row.update(finding_id="F1",severity="High",likelihood="Medium",affected_assets=1,estimated_low_cost=1,estimated_base_cost=2,estimated_high_cost=3,remediation_time_months=2,pre_close_relevance=True,day_1_relevance=False,integration_relevance=True)
    return pd.DataFrame([row])

def test_valid_data(): assert validate_findings(valid_frame())==[]
def test_duplicate_ids():
    frame=pd.concat([valid_frame(),valid_frame()],ignore_index=True)
    assert any("unique" in e for e in validate_findings(frame))
def test_missing_invalid_severity_and_cost_order():
    frame=valid_frame(); frame.loc[0,"title"]=None; frame.loc[0,"severity"]="Extreme"; frame.loc[0,"estimated_low_cost"]=4
    text=" ".join(validate_findings(frame)); assert "missing" in text and "invalid" in text and "low <= base" in text
def test_company_and_zero_ebitda():
    assert len(validate_company({"enterprise_value":0,"ebitda":0}))==2
