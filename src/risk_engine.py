"""Transparent preliminary exposure rating for diligence observations."""

SEVERITY = {"Low": 1, "Medium": 2, "High": 3, "Critical": 4}
LIKELIHOOD = {"Low": 1, "Medium": 2, "High": 3}
CRITICALITY = {"Low": 1, "Medium": 2, "High": 3, "Critical": 4}


def score_finding(finding):
    """Return a screening rating, score and explanation; not a residual-risk opinion."""
    severity = str(finding["severity"])
    likelihood = str(finding["likelihood"])
    criticality = str(finding["business_criticality"])
    assets = max(float(finding.get("affected_assets", 0) or 0), 0)
    breadth = 2 if assets >= 15 else 1 if assets >= 5 else 0
    score = SEVERITY[severity] * 3 + LIKELIHOOD[likelihood] * 2 + CRITICALITY[criticality] * 2 + breadth
    rating = "Critical" if score >= 27 else "High" if score >= 19 else "Medium" if score >= 12 else "Low"
    reasons = [f"{severity.lower()} stated technical severity", f"{likelihood.lower()} assumed likelihood", f"{criticality.lower()} business criticality"]
    if breadth:
        reasons.append(f"reported breadth of {int(assets)} assets")
    explanation = (f"{rating} preliminary exposure because of " + ", ".join(reasons) +
                   f" (screening score {score}). Validate scope, evidence and compensating controls; this is not a residual-risk conclusion.")
    return rating, score, explanation


def enrich_findings(df):
    result = df.copy()
    scored = result.apply(lambda row: score_finding(row), axis=1)
    result[["risk_rating", "risk_score", "risk_explanation"]] = list(scored)
    return result
