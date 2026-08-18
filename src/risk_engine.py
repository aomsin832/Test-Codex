"""Transparent cyber-risk scoring; no probabilistic or hidden inputs."""
SEVERITY = {"Low": 1, "Medium": 2, "High": 3, "Critical": 4}
LIKELIHOOD = {"Low": 1, "Medium": 2, "High": 3}
CRITICALITY = {"Low": 1, "Medium": 2, "High": 3, "Critical": 4}
COMPLEXITY = {"Low": 0, "Medium": 1, "High": 2}


def score_finding(finding):
    """Return (rating, numeric score, plain-English explanation)."""
    severity = str(finding["severity"])
    likelihood = str(finding["likelihood"])
    criticality = str(finding["business_criticality"])
    complexity = str(finding["remediation_complexity"])
    assets = max(float(finding.get("affected_assets", 0) or 0), 0)
    asset_points = 2 if assets >= 15 else 1 if assets >= 5 else 0
    score = SEVERITY[severity] * 3 + LIKELIHOOD[likelihood] * 2 + CRITICALITY[criticality] * 2 + COMPLEXITY[complexity] + asset_points
    rating = "Critical" if score >= 25 else "High" if score >= 19 else "Medium" if score >= 12 else "Low"
    reasons = [f"{severity.lower()} inherent severity", f"{likelihood.lower()} likelihood", f"{criticality.lower()} business criticality"]
    if asset_points:
        reasons.append(f"{int(assets)} affected assets")
    if complexity == "High":
        reasons.append("material remediation complexity")
    explanation = f"{rating} risk because the finding has " + ", ".join(reasons) + f" (rules score {score})."
    return rating, score, explanation


def enrich_findings(df):
    result = df.copy()
    scored = result.apply(lambda row: score_finding(row), axis=1)
    result[["risk_rating", "risk_score", "risk_explanation"]] = list(scored)
    return result
