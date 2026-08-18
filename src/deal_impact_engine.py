"""Rules translating technical findings into transaction implications."""
def map_deal_impact(row):
    impacts=[]
    rating=row.get("risk_rating", row.get("severity"))
    title=(row.get("title") or "").lower(); domain=row.get("cyber_domain", "")
    if bool(row.get("pre_close_relevance")): impacts.append("Pre-close diligence issue")
    if rating == "Critical": impacts += ["Deal-breaker / escalation consideration", "Purchase-price consideration"]
    if bool(row.get("day_1_relevance")): impacts.append("Day-1 requirement")
    if bool(row.get("integration_relevance")): impacts.append("Integration dependency")
    if domain in ("Data Protection", "Third-Party Risk"): impacts.append("SPA / contractual consideration")
    if domain in ("Security Operations", "Data Protection") or "incident" in title: impacts.append("Cyber insurance consideration")
    if float(row.get("remediation_time_months",0) or 0) <= 4: impacts.append("100-day remediation")
    if row.get("remediation_complexity") == "High": impacts.append("Transformation opportunity")
    return list(dict.fromkeys(impacts or ["No material deal impact"]))


def diligence_question(row):
    title=(row.get("title") or "").lower()
    if "erp" in title or "unsupported" in title: return "What is management's funded replacement plan, compensating controls, and expected migration timeline?"
    if "incident" in title: return "When was the last exercise, what gaps were identified, and have related incidents occurred?"
    if "vendor" in title: return "Which critical vendors remain unassessed and are contractual security obligations affected?"
    return "What is the funded remediation plan, target date, accountable owner, and current compensating control?"


def enrich_deal_impacts(df):
    result=df.copy(); result["deal_impacts"]=result.apply(map_deal_impact,axis=1)
    result["ma_implication"]=result["deal_impacts"].apply(lambda x:"; ".join(x))
    result["diligence_question"]=result.apply(diligence_question,axis=1)
    result["recommended_timing"]=result["roadmap_period"]
    result["deal_rationale"]=result.apply(lambda r: f"{r['title']} may affect transaction certainty, integration effort, or post-close expenditure because it affects {r['affected_assets']} asset(s) with {str(r['business_criticality']).lower()} business criticality.",axis=1)
    return result
