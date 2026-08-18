from pathlib import Path

import pytest

from src.summary_engine import executive_summary
from src.target_engine import integration_complexity, load_all_targets, target_comparison_frame
from src.valuation_engine import calculate_sensitivity


TARGET_ROOT = Path("data/targets")


def test_all_synthetic_targets_validate_and_enrich_independently():
    targets = load_all_targets(TARGET_ROOT)
    assert list(targets) == ["atlas", "beacon", "forge", "harbor"]
    for target_id, record in targets.items():
        company, findings, totals = record["company"], record["findings"], record["totals"]
        assert company["fictional"] is True
        assert company["target_id"] == target_id
        assert len(findings) > 0
        assert findings["target_id"].eq(target_id).all()
        assert findings[findings.risk_rating.isin(["High", "Critical"])].diligence_question.str.len().gt(0).all()
        assert totals["Low"] <= totals["Base"] <= totals["High"]


def test_cost_cases_are_ordered_per_finding_and_match_source_aggregation():
    targets = load_all_targets(TARGET_ROOT)
    expected_atlas = {"Low": 3_150_000.0, "Base": 6_320_000.0, "High": 11_110_000.0}
    assert targets["atlas"]["totals"] == expected_atlas
    for record in targets.values():
        findings, totals = record["findings"], record["totals"]
        assert (findings.estimated_low_cost <= findings.estimated_base_cost).all()
        assert (findings.estimated_base_cost <= findings.estimated_high_cost).all()
        assert totals == {
            "Low": float(findings.estimated_low_cost.sum()),
            "Base": float(findings.estimated_base_cost.sum()),
            "High": float(findings.estimated_high_cost.sum()),
        }


def test_target_comparison_financial_calculations_are_independent():
    targets = load_all_targets(TARGET_ROOT)
    comparison = target_comparison_frame(targets).set_index("target_id")
    for target_id, record in targets.items():
        company, totals = record["company"], record["totals"]
        row = comparison.loc[target_id]
        assert row["EV / EBITDA"] == pytest.approx(company["enterprise_value"] / company["ebitda"])
        assert row["Base cost / EV"] == pytest.approx(totals["Base"] / company["enterprise_value"])
        assert row["Base cost / EBITDA"] == pytest.approx(totals["Base"] / company["ebitda"])
        findings = record["findings"]
        assert row["Pre-close items"] == findings.pre_close_relevance.sum()
        assert row["Day 1 items"] == findings.day_1_relevance.sum()
        assert row["First 100-day items"] == findings.delivery_horizon.isin(["Day 30", "Day 100"]).sum()


def test_target_switching_does_not_leak_findings_or_totals():
    targets = load_all_targets(TARGET_ROOT)
    finding_sets = [set(record["findings"].finding_id) for record in targets.values()]
    for index, ids in enumerate(finding_sets):
        assert all(ids.isdisjoint(other) for other in finding_sets[index + 1:])
    assert len({record["totals"]["Base"] for record in targets.values()}) == len(targets)


def test_synthetic_profiles_demonstrate_distinct_learning_cases():
    targets = load_all_targets(TARGET_ROOT)
    atlas, beacon, forge, harbor = (targets[name] for name in ["atlas", "beacon", "forge", "harbor"])
    high_count = lambda record: int(record["findings"].risk_rating.isin(["High", "Critical"]).sum())
    assert beacon["company"]["enterprise_value"] > atlas["company"]["enterprise_value"]
    assert high_count(beacon) < high_count(atlas)
    assert beacon["totals"]["Base"] < atlas["totals"]["Base"]
    assert integration_complexity(beacon["findings"]) == "Lower"
    assert forge["company"]["enterprise_value"] < atlas["company"]["enterprise_value"]
    assert forge["totals"]["Base"] > atlas["totals"]["Base"]
    assert forge["findings"].remediation_time_months.max() >= 24
    privacy_vendor = harbor["findings"].cyber_domain.isin(["Data Protection", "Third-Party Risk"])
    assert privacy_vendor.sum() >= 6
    assert harbor["findings"].pre_close_relevance.sum() >= 6


@pytest.mark.parametrize("scenario", ["Low", "Base", "High"])
@pytest.mark.parametrize("allocation", [0, .25, .5, .75, 1])
def test_every_target_scenario_and_allocation_matches_independent_arithmetic(scenario, allocation):
    for record in load_all_targets(TARGET_ROOT).values():
        company, totals = record["company"], record["totals"]
        cost = totals[scenario]
        expected_ev = company["enterprise_value"] - cost * allocation
        result = calculate_sensitivity(company["enterprise_value"], company["ebitda"], cost, allocation)
        assert result["ev_ebitda"] == pytest.approx(company["enterprise_value"] / company["ebitda"])
        assert result["remediation_ev"] == pytest.approx(cost / company["enterprise_value"])
        assert result["remediation_ebitda"] == pytest.approx(cost / company["ebitda"])
        assert result["illustrative_allocation"] == pytest.approx(cost * allocation)
        assert result["adjusted_ev"] == pytest.approx(expected_ev)
        assert result["adjusted_ev_ebitda"] == pytest.approx(expected_ev / company["ebitda"])


def test_each_executive_summary_uses_its_own_findings_and_totals():
    targets = load_all_targets(TARGET_ROOT)
    summaries = {}
    for target_id, record in targets.items():
        summaries[target_id] = executive_summary(record["findings"], record["company"], record["totals"])
        assert f"${record['totals']['Base']/1e6:.1f}m" in summaries[target_id]
        assert record["findings"].sort_values("risk_score", ascending=False).iloc[0].title in summaries[target_id]
    assert len(set(summaries.values())) == len(targets)
