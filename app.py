"""Streamlit interface for the synthetic Cyber M&A learning proof of concept."""
import pandas as pd
import streamlit as st

from pathlib import Path

from src.remediation_engine import build_integration_roadmap
from src.summary_engine import executive_summary, overall_deal_risk
from src.target_engine import (comparison_summary, integration_complexity, load_all_targets,
                               main_domains, target_comparison_frame, target_investigation_prompts)
from src.valuation_engine import calculate_sensitivity, select_remediation_scenario, sensitivity_table

ROOT = Path(__file__).parent
RISK_ORDER = ["Critical", "High", "Medium", "Low"]
PERIOD_ORDER = ["Pre-close", "Day 1", "Day 30", "Day 100", "6–12 months"]
DELIVERY_ORDER = ["Day 30", "Day 100", "6–12 months", "Longer-term transformation"]


@st.cache_data
def load_data():
    return load_all_targets(ROOT / "data" / "targets")


def money(value):
    return f"${value / 1_000_000:,.1f}m"


def ratio(value):
    return "N/A" if value is None else f"{value:.1%}"


def multiple(value):
    return "N/A" if value is None else f"{value:.1f}x"


def export(label, frame, filename, key):
    st.download_button(label, frame.to_csv(index=False).encode(), filename, "text/csv", key=key)


def material_findings(findings, limit=5):
    return findings.sort_values(["risk_score", "estimated_base_cost"], ascending=False).head(limit)


def show_metrics(company, findings, totals):
    financials = calculate_sensitivity(company["enterprise_value"], company["ebitda"], totals["Base"], 0)
    values = [
        ("Enterprise Value", money(company["enterprise_value"])),
        ("EBITDA", money(company["ebitda"])),
        ("EV / EBITDA", multiple(financials["ev_ebitda"])),
        ("Cyber findings", len(findings)),
        ("High-priority findings", findings.risk_rating.isin(["Critical", "High"]).sum()),
        ("Base synthetic remediation", money(totals["Base"])),
        ("Cost / EV scale", ratio(financials["remediation_ev"])),
        ("Overall diligence priority", overall_deal_risk(findings)),
    ]
    for offset in (0, 4):
        for col, (label, value) in zip(st.columns(4), values[offset:offset + 4]):
            col.metric(label, value)


def finding_translation(item):
    st.markdown(f"#### {item.finding_id} · {item.title}")
    st.caption(f"{item.cyber_domain}  •  {item.risk_rating} preliminary exposure  •  {money(item.estimated_base_cost)} synthetic base estimate  •  {item.remediation_time_months:g} months estimated delivery")
    observation, business = st.columns(2)
    observation.markdown("**Cyber observation**")
    observation.write(item.description)
    business.markdown("**Business implication**")
    business.write(item.deal_rationale)
    transaction, question = st.columns(2)
    transaction.markdown("**Transaction consideration**")
    transaction.write(item.ma_implication)
    question.markdown("**Recommended diligence question**")
    question.write(item.diligence_question)


st.set_page_config(page_title="Cyber M&A Navigator", page_icon="◈", layout="wide")
st.markdown("""<style>
.stApp{background:#f5f7fa}.block-container{padding-top:1.2rem;max-width:1450px}
[data-testid='stMetric']{background:white;border:1px solid #dce3e9;border-top:3px solid #2f607e;padding:14px;border-radius:8px}
.hero{background:linear-gradient(120deg,#102f44,#346b89);padding:25px 30px;border-radius:10px;color:white;margin-bottom:12px}
.hero h1{margin:0 0 4px}.hero h3{margin:0 0 12px;color:#dcebf3}.badge{display:inline-block;background:#e3f0f6;color:#173b50;padding:5px 11px;border-radius:18px;font-weight:700}
.journey{background:white;border:1px solid #dce3e9;padding:13px;text-align:center;border-radius:8px;font-weight:650;color:#244b63;margin:10px 0 18px}
</style>""", unsafe_allow_html=True)
st.markdown("""<div class='hero'><h1>Cyber M&A Due Diligence & Valuation Impact Navigator</h1>
<h3>From cyber finding to deal insight</h3>
<p>Translate cybersecurity diligence observations into remediation priorities, transaction considerations, and illustrative financial sensitivity.</p>
<span class='badge'>Synthetic Deal — Learning POC Only</span></div>""", unsafe_allow_html=True)

try:
    targets = load_data()
except (OSError, ValueError, pd.errors.ParserError) as exc:
    st.error(f"Data could not be loaded: {exc}")
    st.stop()

target_ids = list(targets)
selected_target_id = st.selectbox(
    "Select synthetic acquisition target",
    target_ids,
    format_func=lambda target_id: f"{targets[target_id]['company']['project_name']} — {targets[target_id]['company']['target']} | {targets[target_id]['company']['profile']}",
)
selected_record = targets[selected_target_id]
company, findings, totals = selected_record["company"], selected_record["findings"], selected_record["totals"]
roadmap = build_integration_roadmap(findings)
priority = material_findings(findings)
st.markdown("<div class='journey'>Cyber finding &nbsp;→&nbsp; Remediation requirement &nbsp;→&nbsp; Transaction consideration &nbsp;→&nbsp; Financial sensitivity &nbsp;→&nbsp; Integration action</div>", unsafe_allow_html=True)

tabs = st.tabs(["Overview", "Cyber Findings", "Cyber → M&A", "Remediation", "Financial Sensitivity", "Integration Roadmap", "Executive Summary", "Target Comparison", "Methodology"])

with tabs[0]:
    st.subheader("What is the deal?")
    st.markdown(f"**{company['buyer']}** → **{company['target']}** &nbsp; · &nbsp; {company['industry']} &nbsp; · &nbsp; {company['geography']} &nbsp; · &nbsp; Fictional {company['transaction_type'].lower()}")
    show_metrics(company, findings, totals)
    st.markdown("#### What did cyber diligence identify?")
    st.write(f"The main observed domains are **{', '.join(main_domains(findings))}**. The Base synthetic remediation case is **{money(totals['Base'])}**, subject to evidence, scope, buyer standards and existing investment plans.")
    overview = priority[["finding_id", "title", "cyber_domain", "risk_rating", "estimated_base_cost", "remediation_time_months"]].copy()
    overview.columns = ["ID", "Finding", "Cyber domain", "Preliminary exposure", "Base synthetic estimate", "Delivery months"]
    st.dataframe(overview, hide_index=True, width="stretch", column_config={"Base synthetic estimate": st.column_config.NumberColumn(format="$%d")})
    st.markdown("#### Why does this matter?")
    st.info(f"**{overall_deal_risk(findings)}.** The findings may drive additional evidence requests and a potential investment requirement; the current integration-complexity screen is **{integration_complexity(findings).lower()}**. These are planning prompts, not deal conclusions.")
    st.markdown("#### What happens next?")
    st.markdown("**Pre-close evidence → Day 1 readiness → First 100 days → Longer-term transformation**")

with tabs[1]:
    st.subheader("Priority cyber diligence observations")
    st.caption("The five observations below rank highest under the transparent preliminary-exposure screen; they remain subject to evidence validation.")
    st.info("**Learning point:** A technical finding does not automatically become a transaction issue. Evidence, affected business processes, and deal context matter.")
    for _, item in priority.iterrows():
        with st.container(border=True):
            cols = st.columns([3, 2, 1, 1])
            cols[0].markdown(f"**{item.finding_id} · {item.title}**  \n{item.cyber_domain}")
            cols[1].write(item.deal_rationale)
            cols[2].metric("Exposure", item.risk_rating)
            cols[3].metric("Base / delivery", f"{money(item.estimated_base_cost)}", f"{item.remediation_time_months:g} months", delta_color="off")

    with st.expander("Explore and filter all findings", expanded=False):
        a, b, c, d = st.columns(4)
        domains = a.multiselect("Cyber domain", sorted(findings.cyber_domain.unique()), default=sorted(findings.cyber_domain.unique()))
        risks = b.multiselect("Preliminary exposure", RISK_ORDER, default=RISK_ORDER)
        periods = c.multiselect("Transaction timing", PERIOD_ORDER, default=PERIOD_ORDER)
        impact_options = sorted({impact for impacts in findings.deal_impacts for impact in impacts})
        impacts = d.multiselect("M&A impact", impact_options)
        mask = findings.cyber_domain.isin(domains) & findings.risk_rating.isin(risks) & findings.roadmap_period.isin(periods)
        if impacts:
            mask &= findings.deal_impacts.apply(lambda values: any(impact in values for impact in impacts))
        filtered = findings[mask]
        table = filtered[["finding_id", "title", "cyber_domain", "risk_rating", "roadmap_period", "estimated_base_cost", "remediation_time_months"]].copy()
        table.columns = ["ID", "Finding", "Domain", "Exposure", "Transaction timing", "Base estimate", "Delivery months"]
        st.dataframe(table, hide_index=True, width="stretch", column_config={"Base estimate": st.column_config.NumberColumn(format="$%d")})
        export("Download filtered findings", filtered.drop(columns="deal_impacts"), "cyber_findings_register.csv", "findings")

with tabs[2]:
    st.subheader("Cyber observation → transaction consideration")
    st.caption("Use this view to explain how technical evidence becomes a qualified transaction question—not a definitive deal conclusion.")
    selected_id = st.selectbox("Select a priority finding", priority.finding_id, format_func=lambda item: f"{item} — {priority.set_index('finding_id').loc[item, 'title']}")
    selected = priority[priority.finding_id.eq(selected_id)].iloc[0]
    with st.container(border=True):
        finding_translation(selected)
    st.markdown("#### Buyer and seller perspective")
    buyer, seller = st.columns(2)
    buyer.info(f"**Buyer perspective**\n\nValidate the evidence and scope; assess integration complexity and investment requirements; consider whether specialist, legal, contractual, or insurance review is warranted.\n\n**Current prompt:** {selected.ma_implication}")
    seller.info("**Seller perspective**\n\nProvide stronger evidence, demonstrate compensating controls, clarify existing investment plans and accountable owners, and consider proportionate remediation before close where practical.")

with tabs[3]:
    st.subheader("Synthetic remediation analysis")
    st.caption("Cost cases are synthetic planning assumptions. Transaction timing is the next deal action; delivery horizon is the estimated duration of full remediation.")
    st.info("**Learning point:** A finding may require attention before close even if full technical remediation takes months.")
    for col, scenario in zip(st.columns(3), ["Low", "Base", "High"]):
        col.metric(f"{scenario} synthetic cost case", money(totals[scenario]))
    domain_cost = findings.groupby("cyber_domain").estimated_base_cost.sum().sort_values(ascending=False)
    horizon_cost = findings.groupby("delivery_horizon").estimated_base_cost.sum().reindex(DELIVERY_ORDER, fill_value=0)
    complexity = findings.remediation_complexity.value_counts().reindex(["Low", "Medium", "High"], fill_value=0)
    left, middle, right = st.columns(3)
    left.markdown("#### Base cost by cyber domain")
    left.bar_chart(domain_cost, x_label="Cyber domain", y_label="Synthetic base cost (USD)")
    middle.markdown("#### Base cost by delivery horizon")
    middle.bar_chart(horizon_cost, x_label="Full delivery horizon", y_label="Synthetic base cost (USD)")
    right.markdown("#### Findings by complexity")
    right.bar_chart(complexity, x_label="Remediation complexity", y_label="Findings")
    timing = findings[["finding_id", "title", "roadmap_period", "delivery_horizon", "remediation_time_months"]].copy()
    timing.columns = ["ID", "Finding", "Transaction timing", "Full delivery horizon", "Delivery months"]
    st.markdown("#### Transaction timing versus full remediation")
    st.dataframe(timing, hide_index=True, width="stretch")

with tabs[4]:
    st.subheader("Illustrative Cyber Financial Sensitivity")
    st.info("**Learning point:** Cyber remediation cost can inform transaction economics, but it is not automatically a purchase-price deduction.")
    with st.expander("How to interpret this analysis", expanded=True):
        st.markdown("""1. All remediation estimates are synthetic.
2. Remediation cost is not the same as economic loss.
3. Remediation cost does not automatically reduce Enterprise Value.
4. The allocation slider is only a hypothetical sensitivity assumption.
5. Actual treatment depends on diligence, negotiation, deal structure, accounting, legal analysis, and professional judgment.""")
    a, b, c, d, e = st.columns(5)
    ev = a.number_input("Headline Enterprise Value", min_value=1.0, value=float(company["enterprise_value"]), step=1_000_000.0)
    ebitda = b.number_input("EBITDA", min_value=0.0, value=float(company["ebitda"]), step=1_000_000.0)
    scenario = c.selectbox("Remediation scenario", ["Low", "Base", "High"], index=1)
    planning_factor = d.number_input("Synthetic cost planning factor", min_value=0.0, value=1.0, step=.1, help="Scales the selected synthetic cost case; it is not a probability or valuation multiple.")
    allocation = e.slider("Hypothetical allocation (%)", 0, 100, 0, 25) / 100
    scenario_cost = select_remediation_scenario(totals, scenario)
    result = calculate_sensitivity(ev, ebitda, scenario_cost, allocation, planning_factor)
    outputs = [
        ("Headline EV / EBITDA", multiple(result["ev_ebitda"])),
        ("Selected synthetic remediation cost", money(result["selected_remediation"])),
        ("Cost / EV scale", ratio(result["remediation_ev"])),
        ("Cost / EBITDA scale", ratio(result["remediation_ebitda"])),
        ("Hypothetical transaction allocation", money(result["illustrative_allocation"])),
        ("Illustrative EV", money(result["adjusted_ev"])),
        ("Illustrative EV / EBITDA", multiple(result["adjusted_ev_ebitda"])),
    ]
    for col, (label, value) in zip(st.columns(4), outputs[:4]):
        col.metric(label, value)
    for col, (label, value) in zip(st.columns(3), outputs[4:]):
        col.metric(label, value)
    if result["adjusted_ev"] < 0:
        st.warning("The selected assumptions produce a negative mechanical Illustrative EV. This is outside the meaningful range of this scale sensitivity and must not be interpreted as a negative company value.")
    sensitivity = sensitivity_table(ev, ebitda, scenario_cost, planning_factor)
    st.caption("Cost / EBITDA is a scale indicator only; this POC does not determine accounting treatment.")
    st.line_chart(sensitivity.set_index("Illustrative allocation (%)")["Illustrative EV"], x_label="Hypothetical allocation (%)", y_label="Illustrative EV (USD)")
    export("Download sensitivity table", sensitivity, "valuation_sensitivity.csv", "valuation")

with tabs[5]:
    st.subheader("Transaction and integration roadmap")
    st.caption("Cyber M&A continues after close: diligence questions become readiness decisions, remediation actions, integration dependencies, and longer-term transformation work. Repeated cost references relate to the same finding and must not be added across stages.")
    st.info("**Learning point:** Cyber M&A continues after diligence through Day 1 readiness and post-merger integration.")
    descriptions = {
        "Pre-close": "Evidence and diligence requirements before signing or completion.",
        "Day 1": "Immediate safeguards and readiness decisions.",
        "Day 30": "Initial remediation actions.",
        "Day 100": "Priority integration and security improvements.",
        "6–12 months": "Larger remediation and transformation work.",
        "Longer-term transformation": "Major platform or operating-model change extending beyond 12 months.",
    }
    for period in [*PERIOD_ORDER, "Longer-term transformation"]:
        st.markdown(f"### {period}")
        st.caption(descriptions[period])
        subset = roadmap[roadmap.Stage.eq(period)][["Finding", "Cyber domain", "Action", "Base cost reference", "Complexity", "Business rationale"]]
        if subset.empty:
            st.write("No synthetic actions are assigned to this stage.")
        else:
            st.dataframe(subset, hide_index=True, width="stretch", column_config={"Base cost reference": st.column_config.NumberColumn(format="$%d")})
    export("Download integration roadmap", roadmap, "remediation_roadmap.csv", "roadmap")

with tabs[6]:
    st.subheader("Executive deal-team summary")
    st.markdown(executive_summary(findings, company, totals))
    st.markdown("#### Priority evidence requests")
    st.dataframe(priority[["finding_id", "title", "risk_rating", "diligence_question"]], hide_index=True, width="stretch")

with tabs[7]:
    st.subheader("Synthetic target comparison")
    st.caption("Compare cyber diligence and financial scale across four fictional targets. Cyber is one input to a broader transaction assessment.")
    comparison = target_comparison_frame(targets)
    financial_table = comparison[["Target", "Enterprise Value", "EBITDA", "EV / EBITDA"]].copy()
    financial_table["Enterprise Value"] = financial_table["Enterprise Value"].map(money)
    financial_table["EBITDA"] = financial_table["EBITDA"].map(money)
    financial_table["EV / EBITDA"] = financial_table["EV / EBITDA"].map(multiple)
    cyber_table = comparison[["Target", "Findings", "High / Critical", "Main domains", "Overall diligence priority"]]
    remediation_table = comparison[["Target", "Low remediation", "Base remediation", "High remediation", "Base cost / EV", "Base cost / EBITDA"]].copy()
    for column in ["Low remediation", "Base remediation", "High remediation"]:
        remediation_table[column] = remediation_table[column].map(money)
    for column in ["Base cost / EV", "Base cost / EBITDA"]:
        remediation_table[column] = remediation_table[column].map(ratio)
    transaction_table = comparison[["Target", "Pre-close items", "Day 1 items", "First 100-day items", "Integration complexity"]]
    left, right = st.columns(2)
    left.markdown("#### Financial profile")
    left.dataframe(financial_table, hide_index=True, width="stretch")
    right.markdown("#### Cyber profile")
    right.dataframe(cyber_table, hide_index=True, width="stretch")
    left.markdown("#### Remediation scale")
    left.dataframe(remediation_table, hide_index=True, width="stretch")
    right.markdown("#### Transaction and integration")
    right.dataframe(transaction_table, hide_index=True, width="stretch")
    st.markdown("#### What the synthetic profiles demonstrate")
    st.markdown(comparison_summary(targets, comparison))

    chart_frame = comparison.set_index("Target")
    high_domain = pd.concat([
        record["findings"].assign(Target=record["company"]["target"])[["Target", "cyber_domain"]]
        for record in targets.values()
    ]).groupby(["Target", "cyber_domain"]).size().unstack(fill_value=0)
    a, b = st.columns(2)
    a.markdown("#### Base remediation cost by target")
    a.bar_chart(chart_frame["Base remediation"], x_label="Synthetic target", y_label="Synthetic Base cost (USD)")
    b.markdown("#### Base cost / EV by target")
    b.bar_chart(chart_frame["Base cost / EV"] * 100, x_label="Synthetic target", y_label="Base cost / EV (%)")
    a, b = st.columns(2)
    a.markdown("#### High/Critical findings by target")
    a.bar_chart(chart_frame["High / Critical"], x_label="Synthetic target", y_label="Findings")
    b.markdown("#### Findings by cyber domain")
    b.bar_chart(high_domain, x_label="Synthetic target", y_label="Findings")

    st.markdown("### Compare two targets")
    left, right = st.columns(2)
    target_a_id = left.selectbox("Target A", target_ids, index=0, format_func=lambda item: targets[item]["company"]["target"], key="compare_a")
    target_b_id = right.selectbox("Target B", target_ids, index=3, format_func=lambda item: targets[item]["company"]["target"], key="compare_b")
    for col, label, target_id in [(left, "Target A", target_a_id), (right, "Target B", target_b_id)]:
        record = targets[target_id]
        target_company, target_findings, target_totals = record["company"], record["findings"], record["totals"]
        financials = calculate_sensitivity(target_company["enterprise_value"], target_company["ebitda"], target_totals["Base"], 0)
        full_allocation = calculate_sensitivity(target_company["enterprise_value"], target_company["ebitda"], target_totals["Base"], 1)
        considerations = sorted({impact for impacts in target_findings.deal_impacts for impact in impacts})
        with col.container(border=True):
            st.markdown(f"#### {label} · {target_company['target']}")
            st.caption(f"{target_company['profile']} · {target_company['learning_focus']}")
            st.write(f"**Financial profile:** {money(target_company['enterprise_value'])} EV; {money(target_company['ebitda'])} EBITDA; {multiple(financials['ev_ebitda'])} EV / EBITDA")
            st.write(f"**Cyber exposure:** {len(target_findings)} findings; {target_findings.risk_rating.isin(['High', 'Critical']).sum()} High/Critical")
            st.write(f"**Remediation scale:** {money(target_totals['Base'])} Base; {ratio(financials['remediation_ev'])} of EV; {ratio(financials['remediation_ebitda'])} of EBITDA")
            st.write(f"**Main cyber domains:** {', '.join(main_domains(target_findings))}")
            st.write(f"**Transaction considerations:** {'; '.join(considerations[:4])}")
            st.write(f"**Integration complexity:** {integration_complexity(target_findings)}")
            st.write(f"**Financial sensitivity:** the Base case spans {money(financials['adjusted_ev'])} at 0% to {money(full_allocation['adjusted_ev'])} at 100% hypothetical allocation. This range illustrates arithmetic, not transaction treatment.")
            st.markdown("**What the buyer would investigate further**")
            for question in target_investigation_prompts(record):
                st.markdown(f"- {question}")
    if target_a_id == target_b_id:
        st.info("Select two different targets to compare contrasting profiles.")

with tabs[8]:
    st.subheader("Methodology and limitations")
    st.markdown("""
#### Preliminary exposure
The deterministic screen uses stated technical severity, assumed likelihood, business criticality, and reported asset breadth. It is not a residual-risk conclusion. Remediation complexity does not increase exposure.
#### Remediation assumptions
Low, base, and high values are synthetic, unvalidated planning assumptions—not market benchmarks, quotes, provisions, or necessarily incremental expenditure. Transaction timing and full delivery duration are separate.
#### Roadmap and comparison
A finding may appear at Pre-close, Day 1, and its full-delivery horizon. The Base cost is repeated only as a reference and is not additive across stages. Integration complexity is a simple screen based on integration-relevant findings and High-complexity remediation, not a detailed integration estimate.
#### Transaction considerations
Mappings prompt additional diligence, specialist review, readiness, integration, and cost validation. They do not determine contractual, insurance, price, or transaction outcomes.
#### Illustrative financial sensitivity
Headline EV / EBITDA is EV ÷ EBITDA. Selected cost is scenario cost × planning factor. Hypothetical allocation is allocation percentage × selected cost. Illustrative EV is headline EV − hypothetical allocation. Zero EBITDA returns N/A.
#### Learning scope
All data are synthetic. The POC is deterministic, contains no external API or AI, and requires cyber, financial, legal, insurance, accounting, tax, and transaction-professional judgment.
""")
    st.info("For a guided introduction, read **LEARNING_GUIDE.md**, beginning with sections A–C and the Project Atlas example in section F.")

st.caption("◈ Synthetic Deal — Learning POC Only · Illustrative decision support, not investment advice, a professional valuation, or a cyber due-diligence opinion.")
