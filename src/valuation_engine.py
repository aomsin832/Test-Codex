"""Conservative illustrative financial sensitivities, not valuation conclusions."""

import pandas as pd

SCENARIOS = ("Low", "Base", "High")


def safe_ratio(numerator, denominator):
    """Return a scale ratio, or None where the denominator is not meaningful."""
    return None if denominator is None or denominator <= 0 else float(numerator) / float(denominator)


def select_remediation_scenario(totals, scenario):
    """Select a validated synthetic remediation case from calculated totals."""
    if scenario not in SCENARIOS:
        raise ValueError(f"Scenario must be one of: {', '.join(SCENARIOS)}.")
    missing = [name for name in SCENARIOS if name not in totals]
    if missing:
        raise ValueError("Remediation totals must include Low, Base, and High scenarios.")
    low, base, high = (float(totals[name]) for name in SCENARIOS)
    if min(low, base, high) < 0 or not low <= base <= high:
        raise ValueError("Remediation totals must be non-negative and satisfy Low <= Base <= High.")
    return float(totals[scenario])


def calculate_sensitivity(enterprise_value, ebitda, remediation_cost, allocation_pct, cost_planning_factor=1.0):
    """Calculate scale metrics for a hypothetical allocation of synthetic expenditure."""
    if enterprise_value <= 0:
        raise ValueError("Enterprise value must be greater than zero.")
    if ebitda < 0:
        raise ValueError("EBITDA cannot be negative.")
    if remediation_cost < 0:
        raise ValueError("Remediation cost cannot be negative.")
    if not 0 <= allocation_pct <= 1:
        raise ValueError("Illustrative allocation must be between 0% and 100%.")
    if cost_planning_factor < 0:
        raise ValueError("Planning factor cannot be negative.")

    selected_cost = float(remediation_cost) * float(cost_planning_factor)
    illustrative_allocation = float(allocation_pct) * selected_cost
    illustrative_ev = float(enterprise_value) - illustrative_allocation
    return {
        "headline_ev": float(enterprise_value),
        "ev_ebitda": safe_ratio(enterprise_value, ebitda),
        "selected_remediation": selected_cost,
        "remediation_ev": safe_ratio(selected_cost, enterprise_value),
        "remediation_ebitda": safe_ratio(selected_cost, ebitda),
        "allocation_pct": float(allocation_pct),
        "illustrative_allocation": illustrative_allocation,
        "adjusted_ev": illustrative_ev,
        "adjusted_ev_ebitda": safe_ratio(illustrative_ev, ebitda),
    }


def sensitivity_table(enterprise_value, ebitda, remediation_cost, cost_planning_factor=1.0):
    rows = []
    for pct in range(0, 101, 5):
        result = calculate_sensitivity(enterprise_value, ebitda, remediation_cost, pct / 100, cost_planning_factor)
        rows.append({
            "Illustrative allocation (%)": pct,
            "Hypothetical transaction allocation": result["illustrative_allocation"],
            "Illustrative EV": result["adjusted_ev"],
            "Illustrative EV / EBITDA": result["adjusted_ev_ebitda"],
        })
    return pd.DataFrame(rows)
