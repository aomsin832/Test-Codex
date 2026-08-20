"""Synthetic remediation aggregation and transaction-action sequencing."""
import pandas as pd

COST_COLUMNS = ["estimated_low_cost", "estimated_base_cost", "estimated_high_cost"]


def portfolio_totals(findings):
    return {name: float(findings[column].fillna(0).sum()) for name, column in zip(("Low", "Base", "High"), COST_COLUMNS)}


def roadmap_period(row):
    """Sequence the next transaction action, not promised remediation completion."""
    if bool(row.get("pre_close_relevance")):
        return "Pre-close"
    if bool(row.get("day_1_relevance")):
        return "Day 1"
    months = float(row.get("remediation_time_months", 0) or 0)
    if months <= 1:
        return "Day 30"
    if months <= 4:
        return "Day 100"
    return "6–12 months"


def remediation_category(row):
    period = roadmap_period(row)
    if period == "Pre-close":
        return "Pre-close diligence / deal treatment"
    if period == "Day 1":
        return "Day 1 interim safeguard"
    return f"Remediation planning: {period}"


def full_delivery_horizon(months):
    """Group an estimated delivery duration separately from transaction timing."""
    months = float(months or 0)
    if months <= 1:
        return "Day 30"
    if months <= 4:
        return "Day 100"
    if months <= 12:
        return "6–12 months"
    return "Longer-term transformation"


def add_remediation_analysis(findings):
    result = findings.copy()
    result["remediation_category"] = result.apply(remediation_category, axis=1)
    result["roadmap_period"] = result.apply(roadmap_period, axis=1)
    result["delivery_horizon"] = result["remediation_time_months"].apply(full_delivery_horizon)
    return result


def _action(row):
    if row["roadmap_period"] == "Pre-close":
        return "Validate evidence, exposure and proposed transaction treatment: " + row["title"]
    if row["roadmap_period"] == "Day 1":
        return "Confirm interim safeguard and accountable owner: " + row["title"]
    return "Plan and execute remediation: " + row["title"]


def build_roadmap(findings):
    return findings.assign(
        Action=lambda x: x.apply(_action, axis=1),
        Finding=lambda x: x["finding_id"] + " — " + x["title"],
        Timing=lambda x: x["roadmap_period"],
        **{"Estimated cost": lambda x: x["estimated_base_cost"], "Business rationale": lambda x: x["deal_rationale"]},
    )[["Action", "Finding", "cyber_domain", "Timing", "Estimated cost", "remediation_time_months", "remediation_complexity", "Business rationale"]].rename(
        columns={"cyber_domain": "Cyber domain", "remediation_time_months": "Estimated delivery months", "remediation_complexity": "Complexity"})


def build_integration_roadmap(findings):
    """Build a multi-stage roadmap so diligence actions do not hide later delivery."""
    rows = []
    for _, finding in findings.iterrows():
        common = {
            "Finding": f"{finding['finding_id']} — {finding['title']}",
            "Cyber domain": finding["cyber_domain"],
            "Base cost reference": finding["estimated_base_cost"],
            "Complexity": finding["remediation_complexity"],
            "Business rationale": finding["deal_rationale"],
        }
        if bool(finding["pre_close_relevance"]):
            rows.append({**common, "Stage": "Pre-close", "Action": "Validate evidence, exposure, ownership and potential transaction treatment."})
        if bool(finding["day_1_relevance"]):
            rows.append({**common, "Stage": "Day 1", "Action": "Confirm interim safeguards, continuity requirements and accountable owner."})
        delivery_stage = finding["delivery_horizon"]
        rows.append({
            **common,
            "Stage": delivery_stage,
            "Action": f"Plan and deliver full remediation ({finding['remediation_time_months']:g} month estimate).",
        })
    return pd.DataFrame(rows)[["Stage", "Finding", "Cyber domain", "Action", "Base cost reference", "Complexity", "Business rationale"]]
