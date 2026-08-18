import pytest

from src.valuation_engine import calculate_sensitivity, safe_ratio, select_remediation_scenario, sensitivity_table


def test_required_financial_examples():
    zero = calculate_sensitivity(250_000_000, 20_000_000, 5_000_000, 0)
    half = calculate_sensitivity(250_000_000, 20_000_000, 5_000_000, 0.5)
    full = calculate_sensitivity(250_000_000, 20_000_000, 5_000_000, 1)
    assert zero["ev_ebitda"] == pytest.approx(12.5)
    assert zero["remediation_ev"] == pytest.approx(0.02)
    assert zero["remediation_ebitda"] == pytest.approx(0.25)
    assert zero["adjusted_ev"] == 250_000_000
    assert half["illustrative_allocation"] == 2_500_000
    assert half["adjusted_ev"] == 247_500_000
    assert half["adjusted_ev_ebitda"] == pytest.approx(12.375)
    assert full["adjusted_ev"] == 245_000_000
    assert full["adjusted_ev_ebitda"] == pytest.approx(12.25)


def test_low_base_high_scenario_selection():
    totals = {"Low": 3_000_000, "Base": 5_000_000, "High": 8_000_000}
    assert [select_remediation_scenario(totals, name) for name in ("Low", "Base", "High")] == [3_000_000, 5_000_000, 8_000_000]
    with pytest.raises(ValueError, match="Scenario"):
        select_remediation_scenario(totals, "Expected")


def test_scenario_selection_rejects_missing_or_unordered_totals():
    with pytest.raises(ValueError, match="include"):
        select_remediation_scenario({"Low": 1, "Base": 2}, "Base")
    with pytest.raises(ValueError, match="Low <= Base <= High"):
        select_remediation_scenario({"Low": 3, "Base": 2, "High": 4}, "Base")


def test_zero_ebitda_returns_na_ratios_without_changing_arithmetic():
    result = calculate_sensitivity(250_000_000, 0, 5_000_000, 0.5)
    assert result["ev_ebitda"] is None and result["remediation_ebitda"] is None and result["adjusted_ev_ebitda"] is None
    assert result["adjusted_ev"] == 247_500_000


def test_zero_remediation_leaves_ev_unchanged_at_any_allocation():
    result = calculate_sensitivity(250_000_000, 20_000_000, 0, 1)
    assert result["remediation_ev"] == 0 and result["remediation_ebitda"] == 0
    assert result["illustrative_allocation"] == 0 and result["adjusted_ev"] == 250_000_000
    assert result["adjusted_ev_ebitda"] == 12.5


def test_very_high_remediation_is_shown_as_arithmetic_not_silently_clamped():
    result = calculate_sensitivity(10, 2, 20, 1)
    assert result["illustrative_allocation"] == 20
    assert result["adjusted_ev"] == -10
    assert result["adjusted_ev_ebitda"] == -5


@pytest.mark.parametrize("args, message", [
    ((-1, 20, 5, 0.5), "Enterprise value"), ((10, -1, 5, 0.5), "EBITDA"),
    ((10, 2, -1, 0.5), "Remediation"), ((10, 2, 1, -0.01), "allocation"),
    ((10, 2, 1, 1.01), "allocation"), ((10, 2, 1, 0.5, -1), "Planning factor"),
])
def test_negative_values_and_out_of_range_allocations_are_rejected(args, message):
    with pytest.raises(ValueError, match=message):
        calculate_sensitivity(*args)


def test_planning_factor_scales_cost_before_hypothetical_allocation():
    result = calculate_sensitivity(250_000_000, 20_000_000, 5_000_000, 0.5, 1.2)
    assert result["selected_remediation"] == 6_000_000
    assert result["illustrative_allocation"] == 3_000_000
    assert result["adjusted_ev"] == 247_000_000


def test_sensitivity_table_uses_zero_to_full_allocation():
    table = sensitivity_table(250_000_000, 20_000_000, 5_000_000)
    assert len(table) == 21
    assert table.iloc[0]["Illustrative allocation (%)"] == 0
    assert table.iloc[0]["Illustrative EV"] == 250_000_000
    assert table.iloc[0]["Illustrative EV / EBITDA"] == 12.5
    assert table.iloc[-1]["Illustrative allocation (%)"] == 100
    assert table.iloc[-1]["Illustrative EV"] == 245_000_000


def test_safe_ratio():
    assert safe_ratio(0, 10) == 0
    assert safe_ratio(1, 0) is None
