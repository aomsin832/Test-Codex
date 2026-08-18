"""Validation for the synthetic deal and finding register."""
REQUIRED=["finding_id","title","cyber_domain","description","severity","likelihood","affected_assets","business_criticality","remediation_complexity","estimated_low_cost","estimated_base_cost","estimated_high_cost","remediation_time_months","pre_close_relevance","day_1_relevance","integration_relevance"]
VALID_SEVERITIES={"Low","Medium","High","Critical"}; VALID_LIKELIHOODS={"Low","Medium","High"}

def validate_company(company):
    errors=[]
    if company.get("enterprise_value",0)<=0: errors.append("Enterprise value must be greater than zero.")
    if company.get("ebitda",0)<=0: errors.append("EBITDA must be greater than zero to calculate multiples.")
    return errors

def validate_findings(df):
    errors=[]
    missing_cols=[c for c in REQUIRED if c not in df.columns]
    if missing_cols: return ["Missing required columns: " + ", ".join(missing_cols)]
    if df["finding_id"].duplicated().any(): errors.append("Finding IDs must be unique.")
    for col in REQUIRED:
        if df[col].isna().any() or (df[col].dtype == object and df[col].astype(str).str.strip().eq("").any()): errors.append(f"Required field '{col}' contains missing values.")
    if not set(df["severity"].dropna()).issubset(VALID_SEVERITIES): errors.append("Severity contains an invalid value.")
    if not set(df["likelihood"].dropna()).issubset(VALID_LIKELIHOODS): errors.append("Likelihood contains an invalid value.")
    costs=df[["estimated_low_cost","estimated_base_cost","estimated_high_cost"]]
    if (costs.fillna(0)<0).any().any(): errors.append("Remediation costs cannot be negative.")
    valid_order=(df["estimated_low_cost"]<=df["estimated_base_cost"]) & (df["estimated_base_cost"]<=df["estimated_high_cost"])
    if not valid_order.fillna(False).all(): errors.append("Costs must satisfy low <= base <= high.")
    if (df["affected_assets"].fillna(-1)<0).any(): errors.append("Affected assets cannot be negative.")
    return errors

def validate_all(company, findings): return validate_company(company)+validate_findings(findings)
