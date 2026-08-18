"""Loading and comparison orchestration for synthetic acquisition targets."""
from pathlib import Path
import json

import pandas as pd

from .data_validation import validate_all
from .deal_impact_engine import enrich_deal_impacts
from .remediation_engine import add_remediation_analysis, portfolio_totals
from .risk_engine import enrich_findings
from .summary_engine import overall_deal_risk
from .valuation_engine import calculate_sensitivity

BOOLEAN_COLUMNS = ["pre_close_relevance", "day_1_relevance", "integration_relevance"]


def load_target(directory):
    """Load, validate, and enrich one target directory."""
    directory = Path(directory)
    with (directory / "company.json").open(encoding="utf-8") as handle:
        company = json.load(handle)
    findings = pd.read_csv(directory / "findings.csv")
    for column in BOOLEAN_COLUMNS:
        findings[column] = findings[column].astype(bool)
    errors = validate_all(company, findings)
    if company.get("fictional") is not True:
        errors.append("Target must be explicitly marked fictional.")
    if not company.get("target_id"):
        errors.append("Target must define target_id.")
    if errors:
        raise ValueError(f"{directory.name}: " + " | ".join(errors))
    enriched = enrich_deal_impacts(add_remediation_analysis(enrich_findings(findings)))
    enriched["target_id"] = company["target_id"]
    return {"company": company, "findings": enriched, "totals": portfolio_totals(enriched)}


def load_all_targets(root):
    """Discover target folders, ensuring IDs are unique and ordering is stable."""
    records = [load_target(path) for path in Path(root).iterdir() if path.is_dir()]
    records.sort(key=lambda record: (record["company"].get("display_order", 999), record["company"]["target"]))
    targets = {record["company"]["target_id"]: record for record in records}
    if len(targets) != len(records):
        raise ValueError("Target IDs must be unique.")
    if not targets:
        raise ValueError("No synthetic targets were found.")
    return targets


def integration_complexity(findings):
    relevant = findings[findings["integration_relevance"]]
    high = (relevant["remediation_complexity"] == "High").sum()
    if high >= 3:
        return "High"
    if high or len(relevant) > 6:
        return "Moderate"
    return "Lower"


def target_comparison_frame(targets):
    """Build target-level metrics using the same deterministic engines as target views."""
    rows = []
    for target_id, record in targets.items():
        company, findings, totals = record["company"], record["findings"], record["totals"]
        financials = calculate_sensitivity(company["enterprise_value"], company["ebitda"], totals["Base"], 0)
        rows.append({
            "target_id": target_id,
            "Target": company["target"],
            "Project": company["project_name"],
            "Profile": company["profile"],
            "Enterprise Value": company["enterprise_value"],
            "EBITDA": company["ebitda"],
            "EV / EBITDA": financials["ev_ebitda"],
            "Findings": len(findings),
            "High / Critical": int(findings["risk_rating"].isin(["High", "Critical"]).sum()),
            "Main domains": ", ".join(main_domains(findings)),
            "Low remediation": totals["Low"],
            "Base remediation": totals["Base"],
            "High remediation": totals["High"],
            "Base cost / EV": financials["remediation_ev"],
            "Base cost / EBITDA": financials["remediation_ebitda"],
            "Pre-close items": int(findings["pre_close_relevance"].sum()),
            "Day 1 items": int(findings["day_1_relevance"].sum()),
            "First 100-day items": int(findings["delivery_horizon"].isin(["Day 30", "Day 100"]).sum()),
            "Integration complexity": integration_complexity(findings),
            "Overall diligence priority": overall_deal_risk(findings),
        })
    return pd.DataFrame(rows)


def main_domains(findings, limit=3):
    return findings.groupby("cyber_domain").size().sort_values(ascending=False).head(limit).index.tolist()


def comparison_summary(targets, frame):
    """Generate a deterministic, non-recommendatory cross-target narrative."""
    highest_multiple = frame.loc[frame["EV / EBITDA"].idxmax()]
    highest_investment = frame.loc[frame["Base cost / EV"].idxmax()]
    lowest_exposure = frame.loc[frame["High / Critical"].idxmin()]
    privacy_scores = {
        target_id: record["findings"]["cyber_domain"].isin(["Data Protection", "Third-Party Risk"]).sum()
        for target_id, record in targets.items()
    }
    privacy_id = max(privacy_scores, key=privacy_scores.get)
    privacy = frame.set_index("target_id").loc[privacy_id]
    return (
        f"**{highest_investment['Target']}** has the largest Base cyber cost relative to headline EV ({highest_investment['Base cost / EV']:.1%}), illustrating a proportionately greater remediation and integration requirement in this synthetic set. "
        f"**{lowest_exposure['Target']}** has the fewest High/Critical observations, while **{highest_multiple['Target']}** has the highest headline acquisition multiple; stronger cyber posture does not determine whether that multiple is appropriate. "
        f"**{privacy['Target']}** has the greatest concentration of Data Protection and Third-Party Risk observations, so evidence, privacy, vendor, and contractual diligence may matter more than technical remediation cost alone.\n\n"
        "This synthetic comparison demonstrates how cybersecurity can affect diligence, integration planning, and illustrative financial sensitivity alongside commercial, financial, legal, tax, operational, and other transaction considerations. It does not recommend a target or treat cyber as the sole investment decision."
    )


def target_investigation_prompts(record, limit=3):
    """Return concise evidence questions for a target comparison panel."""
    findings = record["findings"].sort_values(["risk_score", "estimated_base_cost"], ascending=False)
    return findings.head(limit)["diligence_question"].tolist()
