"""Synthetic remediation aggregation and deterministic roadmap rules."""
COST_COLUMNS = ["estimated_low_cost", "estimated_base_cost", "estimated_high_cost"]


def portfolio_totals(findings):
    return {name: float(findings[column].fillna(0).sum()) for name, column in zip(("Low", "Base", "High"), COST_COLUMNS)}


def remediation_category(row):
    if bool(row.get("pre_close_relevance")) and row.get("risk_rating") == "Critical": return "Pre-close consideration"
    if bool(row.get("day_1_relevance")): return "Day 1"
    months = float(row.get("remediation_time_months", 0) or 0)
    if months <= 1: return "Immediate"
    if months <= 4: return "First 100 days"
    if months <= 12: return "6–12 month transformation"
    return "Long-term improvement"


def roadmap_period(row):
    if bool(row.get("pre_close_relevance")) and row.get("risk_rating") == "Critical": return "Pre-close"
    if bool(row.get("day_1_relevance")): return "Day 1"
    months = float(row.get("remediation_time_months", 0) or 0)
    if months <= 1: return "Day 30"
    if months <= 4: return "Day 100"
    return "6–12 months"


def add_remediation_analysis(findings):
    result = findings.copy()
    result["remediation_category"] = result.apply(remediation_category, axis=1)
    result["roadmap_period"] = result.apply(roadmap_period, axis=1)
    return result


def build_roadmap(findings):
    return findings.assign(
        Action=lambda x: "Remediate: " + x["title"],
        Finding=lambda x: x["finding_id"] + " — " + x["title"],
        Timing=lambda x: x["roadmap_period"],
        **{"Estimated cost": lambda x: x["estimated_base_cost"], "Business rationale": lambda x: x["deal_rationale"]},
    )[["Action", "Finding", "cyber_domain", "Timing", "Estimated cost", "remediation_complexity", "Business rationale"]].rename(columns={"cyber_domain":"Cyber domain", "remediation_complexity":"Complexity"})
