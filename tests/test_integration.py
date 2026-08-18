import json
import pandas as pd
from src.data_validation import validate_all
from src.risk_engine import enrich_findings
from src.remediation_engine import add_remediation_analysis, portfolio_totals
from src.deal_impact_engine import enrich_deal_impacts

def test_synthetic_dataset_end_to_end():
    company=json.load(open("data/target_company.json",encoding="utf-8")); findings=pd.read_csv("data/cyber_findings.csv")
    assert validate_all(company,findings)==[]
    output=enrich_deal_impacts(add_remediation_analysis(enrich_findings(findings)))
    assert len(output)==14 and portfolio_totals(output)["Low"] <= portfolio_totals(output)["Base"] <= portfolio_totals(output)["High"]
    assert output[output.risk_rating.isin(["High","Critical"])].diligence_question.str.len().gt(0).all()
