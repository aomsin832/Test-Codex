"""Illustrative valuation sensitivities—not purchase-price recommendations."""

def safe_ratio(numerator, denominator):
    return None if denominator is None or denominator <= 0 else float(numerator) / float(denominator)


def calculate_sensitivity(enterprise_value, ebitda, remediation_cost, adjustment_pct, contingency_multiplier=1.0):
    if enterprise_value <= 0: raise ValueError("Enterprise value must be greater than zero.")
    if ebitda < 0: raise ValueError("EBITDA cannot be negative.")
    if remediation_cost < 0: raise ValueError("Remediation cost cannot be negative.")
    if not 0 <= adjustment_pct <= 1: raise ValueError("Valuation adjustment must be between 0% and 100%.")
    if contingency_multiplier < 0: raise ValueError("Contingency multiplier cannot be negative.")
    selected = remediation_cost * contingency_multiplier
    adjusted_ev = enterprise_value - adjustment_pct * selected
    return {"headline_ev": enterprise_value, "ev_ebitda": safe_ratio(enterprise_value, ebitda), "selected_remediation": selected,
            "remediation_ev": safe_ratio(selected, enterprise_value), "remediation_ebitda": safe_ratio(selected, ebitda),
            "adjusted_ev": adjusted_ev, "adjusted_ev_ebitda": safe_ratio(adjusted_ev, ebitda)}


def sensitivity_table(enterprise_value, ebitda, remediation_cost, contingency_multiplier=1.0):
    import pandas as pd
    rows=[]
    for pct in range(0,101,5):
        r=calculate_sensitivity(enterprise_value,ebitda,remediation_cost,pct/100,contingency_multiplier)
        rows.append({"Adjustment percentage":pct,"Illustrative adjusted EV":r["adjusted_ev"],"Adjusted EV / EBITDA":r["adjusted_ev_ebitda"]})
    return pd.DataFrame(rows)
