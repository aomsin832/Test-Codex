"""Rules translating technical observations into qualified transaction prompts."""

def map_deal_impact(row):
    impacts = []
    rating = row.get("risk_rating", row.get("severity"))
    domain = row.get("cyber_domain", "")
    if bool(row.get("pre_close_relevance")):
        impacts.append("Additional pre-close diligence")
    if rating == "Critical":
        impacts.append("Specialist escalation pending evidence")
    if bool(row.get("day_1_relevance")):
        impacts.append("Day 1 safeguard / readiness planning")
    if bool(row.get("integration_relevance")):
        impacts.append("Integration planning dependency")
    if domain == "Data Protection":
        impacts.append("Legal / privacy assessment may be required")
    if domain == "Third-Party Risk":
        impacts.append("Contract and concentration review may be required")
    if domain == "Security Operations":
        impacts.append("Incident and insurance evidence review")
    if row.get("remediation_complexity") == "High":
        impacts.append("Standalone and integration cost validation")
    return list(dict.fromkeys(impacts or ["Post-close improvement; no specific deal treatment indicated"]))


QUESTIONS = {
    "Identity & Access Management": "Provide the privileged-account population, exceptions, authentication paths and evidence of compensating controls; which accounts must be contained before access is connected?",
    "Infrastructure Security": "Which assets and versions are affected, are they internet-facing or business-critical, what exploit/patch evidence exists, and what funded containment or replacement plan is approved?",
    "Security Operations": "Provide log-source coverage, retention and alert-use-case evidence plus exercise results and material incident history; which detection or response gaps affect Day 1 readiness?",
    "Data Protection": "Which data sets, jurisdictions and systems are in scope, what encryption and key-management evidence exists, and has privacy counsel assessed notification, contractual or regulatory exposure?",
    "Third-Party Risk": "Identify the affected critical vendors, services, data access, assessment status, concentration and relevant contract rights; are any known deficiencies or incidents unresolved?",
    "Governance": "Provide approved ownership, exception decisions, overdue items and board reporting; which gaps represent documentation weakness versus ineffective control operation?",
    "Application Security": "Which products and release paths are affected, what testing evidence and unresolved vulnerabilities exist, and how would buyer tooling and release governance change the cost estimate?",
    "Resilience": "Provide recovery objectives, dependency maps and test evidence, including exceptions and actual recovery results; can critical services meet transaction Day 1 continuity needs?",
    "Cloud Security": "Provide the complete tenant/subscription inventory, uncovered scope, material misconfigurations and monitoring evidence; what must be baselined before environments are interconnected?",
}


def diligence_question(row):
    title = str(row.get("title", "")).lower()
    if "mfa" in title or "shared administrator" in title:
        return "What percentage and number of privileged accounts are affected, which authentication paths bypass MFA, what compensating controls operate, and have related misuse or incidents occurred?"
    if "unsupported" in title or "obsolete" in title or "replacement plan" in title:
        return "When did vendor security support end, which revenue-generating or critical processes depend on the platform, what compensating controls exist, and is replacement approved and budgeted?"
    if "patch" in title:
        return "Which exploitable overdue vulnerabilities affect internet-facing or critical assets, what exceptions and compensating controls apply, and have related incidents occurred?"
    if "contract" in title or "obligation" in title:
        return "Which customer or supplier security and notification clauses may be affected, has counsel assessed exposure, and who owns remediation or disclosure decisions?"
    if "incident" in title:
        return "Provide the incident chronology, affected systems and data, containment evidence, notifications, insurance correspondence, root cause and open actions; what remains uncorroborated?"
    if "recovery" in title or "disaster" in title:
        return "Which revenue-generating services and dependencies were excluded from testing, what recovery objectives were actually achieved, and which Day 1 continuity safeguards are required?"
    if "vendor" in title or "third-party" in title or "processor" in title:
        return "Which critical vendors, data flows and services are affected, what assessment and incident evidence is missing, and what audit, notification, termination or remediation rights exist?"
    return QUESTIONS.get(row.get("cyber_domain"), "What evidence substantiates scope and exposure, what compensating controls operate, and who owns the costed response plan?")


def enrich_deal_impacts(df):
    result = df.copy()
    result["deal_impacts"] = result.apply(map_deal_impact, axis=1)
    result["ma_implication"] = result["deal_impacts"].apply(lambda x: "; ".join(x))
    result["diligence_question"] = result.apply(diligence_question, axis=1)
    result["recommended_timing"] = result["roadmap_period"]
    result["deal_rationale"] = result.apply(
        lambda r: f"The reported scope ({r['affected_assets']} asset(s)) and {str(r['business_criticality']).lower()} business criticality may affect readiness, integration effort or expenditure. Confirm evidence, control effectiveness and buyer operating-model overlap before determining deal treatment.", axis=1)
    return result
