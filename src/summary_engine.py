"""Deterministic, qualified executive narrative generation."""


def overall_deal_risk(findings):
    critical = (findings["risk_rating"] == "Critical").sum()
    high = (findings["risk_rating"] == "High").sum()
    return "Heightened diligence priority" if critical or high >= 3 else "Moderate diligence priority" if high else "Lower diligence priority"


def _titles(frame, limit=3):
    titles = frame.sort_values("risk_score", ascending=False).head(limit)["title"].tolist()
    return ", ".join(titles) if titles else "no separately identified items"


def executive_summary(findings, company, totals):
    """Return a concise deal-team briefing without recommending transaction treatment."""
    from .valuation_engine import safe_ratio

    material = findings[findings["risk_rating"].isin(["Critical", "High"])]
    domains = material.groupby("cyber_domain").size().sort_values(ascending=False).head(3).index.tolist()
    pre_close = findings[findings["pre_close_relevance"]]
    day_one = findings[findings["day_1_relevance"]]
    first_100 = findings[findings["delivery_horizon"].isin(["Day 30", "Day 100"])]
    pct_ev = safe_ratio(totals["Base"], company["enterprise_value"])
    pct_ebitda = safe_ratio(totals["Base"], company["ebitda"])

    return (
        f"**Overall diligence priority: {overall_deal_risk(findings)}**\n\n"
        f"**Priority observations.** {_titles(material)}. The higher-priority observations are concentrated in {', '.join(domains)}.\n\n"
        f"**Before close.** Obtain stronger evidence on {_titles(pre_close)} and validate scope, compensating controls, incidents, ownership, and existing investment plans.\n\n"
        f"**Day 1 readiness.** Confirm interim safeguards and accountable owners for {_titles(day_one)}. "
        f"**First 100 days.** Current transaction sequencing identifies {_titles(first_100)}; pre-close and Day 1 items may also continue as longer remediation programmes after completion.\n\n"
        f"**Synthetic cost scale.** The unvalidated base remediation case is ${totals['Base']/1e6:.1f}m ({pct_ev:.1%} of Enterprise Value and {pct_ebitda:.1%} of annual EBITDA). "
        "These ratios show scale only. Expenditure may be operating, capital, one-time, recurring, internal, or already budgeted; the POC does not determine accounting treatment or economic loss.\n\n"
        "Findings may inform further diligence, the buyer investment case, completion conditions, representations and warranties, indemnities, escrow or other protections, remediation commitments, integration budgets, management plans, insurance review, or price discussions. "
        "No observation or cost estimate determines a transaction outcome or price recommendation. **Human review required.**"
    )
