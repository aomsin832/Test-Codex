"""Deterministic executive narrative generation."""
def overall_deal_risk(findings):
    critical=(findings["risk_rating"]=="Critical").sum(); high=(findings["risk_rating"]=="High").sum()
    return "Severe" if critical>=2 else "Elevated" if critical or high>=3 else "Moderate" if high else "Lower"

def executive_summary(findings, company, totals):
    from .valuation_engine import safe_ratio
    material=findings[findings["risk_rating"].isin(["Critical","High"])]
    domains=material.groupby("cyber_domain").size().sort_values(ascending=False).head(3).index.tolist()
    pre=findings[findings["pre_close_relevance"]].sort_values("risk_score",ascending=False).head(3)["title"].tolist()
    post=findings[findings["day_1_relevance"] | findings["integration_relevance"]].sort_values("risk_score",ascending=False).head(3)["title"].tolist()
    pct_ev=safe_ratio(totals["Base"],company["enterprise_value"]); pct_ebitda=safe_ratio(totals["Base"],company["ebitda"])
    return (f"**Overall Cyber Deal Risk: {overall_deal_risk(findings)}**\n\nThe fictional target has {len(findings)} identified cybersecurity findings, including {len(material)} High/Critical items. "
            f"Base-case remediation is estimated at ${totals['Base']/1e6:.1f}m, equivalent to {pct_ev:.1%} of enterprise value and {pct_ebitda:.1%} of annual EBITDA.\n\n"
            f"The most material issues relate to {', '.join(domains)}. Priority pre-close diligence should focus on {', '.join(pre)}. "
            f"Key post-close priorities include {', '.join(post)}.\n\n**Human review required. POC output is illustrative only.**")
