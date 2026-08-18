"""Polished Streamlit interface for the synthetic Cyber M&A proof of concept."""
from pathlib import Path
import json
import pandas as pd
import streamlit as st

from src.data_validation import validate_all
from src.deal_impact_engine import enrich_deal_impacts
from src.remediation_engine import add_remediation_analysis, build_roadmap, portfolio_totals
from src.risk_engine import enrich_findings
from src.summary_engine import executive_summary, overall_deal_risk
from src.valuation_engine import calculate_sensitivity, sensitivity_table

ROOT = Path(__file__).parent
RISK_ORDER = ["Critical", "High", "Medium", "Low"]
PERIOD_ORDER = ["Pre-close", "Day 1", "Day 30", "Day 100", "6–12 months"]


@st.cache_data
def load_data():
    with (ROOT / "data/target_company.json").open(encoding="utf-8") as handle:
        company = json.load(handle)
    findings = pd.read_csv(ROOT / "data/cyber_findings.csv")
    for column in ["pre_close_relevance", "day_1_relevance", "integration_relevance"]:
        findings[column] = findings[column].astype(bool)
    errors = validate_all(company, findings)
    if errors:
        raise ValueError(" | ".join(errors))
    return company, enrich_deal_impacts(add_remediation_analysis(enrich_findings(findings)))


def money(value): return f"${value / 1_000_000:,.1f}m"
def ratio(value): return "N/A" if value is None else f"{value:.1%}"
def multiple(value): return "N/A" if value is None else f"{value:.1f}x"


def export(label, frame, filename, key):
    st.download_button(label, frame.to_csv(index=False).encode(), filename, "text/csv", key=key)


def disclaimer():
    st.info("**Human review required. POC output is illustrative only.** Not investment advice, a professional valuation, or a cyber due-diligence opinion.")


def show_metrics(company, findings, totals):
    values = [("Enterprise Value", money(company["enterprise_value"])), ("EBITDA", money(company["ebitda"])),
              ("EV / EBITDA", multiple(company["enterprise_value"] / company["ebitda"])), ("Cyber Findings", len(findings)),
              ("Critical / High", findings.risk_rating.isin(["Critical", "High"]).sum()), ("Base Remediation", money(totals["Base"])),
              ("Remediation / EV", ratio(totals["Base"] / company["enterprise_value"])), ("Overall Deal Risk", overall_deal_risk(findings))]
    for offset in (0, 4):
        for col, (label, value) in zip(st.columns(4), values[offset:offset + 4]): col.metric(label, value)


def filter_findings(findings):
    with st.container(border=True):
        a, b, c, d = st.columns(4)
        risks = a.multiselect("Cyber risk", RISK_ORDER, default=RISK_ORDER)
        domains = b.multiselect("Cyber domain", sorted(findings.cyber_domain.unique()), default=sorted(findings.cyber_domain.unique()))
        periods = c.multiselect("Remediation timing", PERIOD_ORDER, default=PERIOD_ORDER)
        all_impacts = sorted({item for items in findings.deal_impacts for item in items})
        impacts = d.multiselect("M&A impact", all_impacts)
        a, b, c = st.columns(3)
        ceiling = int(findings.estimated_base_cost.max())
        cost = a.slider("Maximum base cost", 0, ceiling, ceiling, 50000, format="$%d")
        pre = b.selectbox("Pre-close relevance", ["All", "Yes", "No"])
        day = c.selectbox("Day-1 relevance", ["All", "Yes", "No"])
    mask = findings.risk_rating.isin(risks) & findings.cyber_domain.isin(domains) & findings.roadmap_period.isin(periods) & (findings.estimated_base_cost <= cost)
    if impacts: mask &= findings.deal_impacts.apply(lambda values: any(item in values for item in impacts))
    if pre != "All": mask &= findings.pre_close_relevance.eq(pre == "Yes")
    if day != "All": mask &= findings.day_1_relevance.eq(day == "Yes")
    return findings[mask]


st.set_page_config(page_title="Cyber M&A Navigator", page_icon="◈", layout="wide")
st.markdown("<style>.stApp{background:#f6f8fb}.block-container{padding-top:1.4rem;max-width:1500px}[data-testid='stMetric']{background:white;border:1px solid #dde3ea;border-top:3px solid #315b7d;padding:15px;border-radius:7px}.hero{background:linear-gradient(120deg,#102d42,#315b7d);padding:24px 30px;border-radius:10px;color:white}.badge{background:#dbe9f3;color:#16384f;padding:5px 10px;border-radius:20px;font-weight:700}</style>", unsafe_allow_html=True)
st.markdown("<div class='hero'><h1>Cyber M&A Due Diligence & Valuation Impact Navigator</h1><p>Proof of Concept — Translating Cyber Risk into M&A and Valuation Insights</p><span class='badge'>Synthetic Deal — Demonstration Only</span></div>", unsafe_allow_html=True)
try:
    company, findings = load_data()
except (OSError, ValueError, pd.errors.ParserError) as exc:
    st.error(f"Data could not be loaded: {exc}"); st.stop()
totals = portfolio_totals(findings)
roadmap = build_roadmap(findings)
tabs = st.tabs(["Deal Overview", "Cyber Due Diligence", "M&A Impact", "Valuation Sensitivity", "100-Day Roadmap", "Executive Summary", "Methodology"])

with tabs[0]:
    st.subheader(f"{company['project_name']} | {company['buyer']} → {company['target']}")
    st.caption("All names, organizations, findings, incidents, and financial information are fictional.")
    show_metrics(company, findings, totals)
    left, right = st.columns(2)
    snapshot = pd.DataFrame({"Attribute": ["Transaction", "Industry", "Geography", "Revenue", "Employees", "Applications / critical", "Cloud", "Customer data"],
                             "Fictional value": [company["transaction_type"], company["industry"], company["geography"], money(company["revenue"]), f"{company['employees']:,}", f"{company['technology_applications']} / {company['critical_applications']}", company["cloud_environment"], "Yes"]})
    left.markdown("#### Transaction snapshot"); left.dataframe(snapshot, hide_index=True, width="stretch")
    chart = findings.groupby("risk_rating", as_index=False).size()
    right.markdown("#### Risk profile"); right.bar_chart(chart.set_index("risk_rating")["size"], x_label="Risk", y_label="Findings")
    disclaimer()

with tabs[1]:
    st.subheader("Cyber Due-Diligence Findings")
    filtered = filter_findings(findings)
    if filtered.empty:
        st.warning("No findings match the selected filters. Adjust the filters to continue.")
    else:
        columns = ["finding_id", "title", "cyber_domain", "severity", "risk_rating", "remediation_category", "estimated_base_cost", "ma_implication"]
        st.dataframe(filtered[columns], hide_index=True, width="stretch", column_config={"estimated_base_cost": st.column_config.NumberColumn("Base remediation", format="$%d")})
        export("Download Cyber Findings Register", filtered.drop(columns="deal_impacts"), "cyber_findings_register.csv", "findings")
        a, b = st.columns(2)
        a.markdown("#### Findings by risk"); a.bar_chart(filtered.risk_rating.value_counts().reindex(RISK_ORDER, fill_value=0))
        domain_cost = filtered.groupby("cyber_domain", as_index=False).estimated_base_cost.sum()
        b.markdown("#### Base remediation by domain"); b.bar_chart(domain_cost.set_index("cyber_domain"))
        a, b = st.columns(2)
        a.markdown("#### Findings by domain"); a.bar_chart(filtered.cyber_domain.value_counts())
        b.markdown("#### Findings by timeline"); b.bar_chart(filtered.roadmap_period.value_counts().reindex(PERIOD_ORDER, fill_value=0))
        choice = st.selectbox("Select a finding for detailed analysis", filtered.finding_id, format_func=lambda item: f"{item} — {filtered.set_index('finding_id').loc[item, 'title']}")
        item = filtered.set_index("finding_id").loc[choice]
        with st.container(border=True):
            st.markdown(f"### {item.title}\n{item.description}")
            st.write(f"**Rules-based rating:** {item.risk_explanation}")
            st.write(f"**M&A implications:** {item.ma_implication}")
            st.write(f"**Why it matters:** {item.deal_rationale}")
            st.write(f"**Management question:** {item.diligence_question}")
            st.write(f"**Cost range:** {money(item.estimated_low_cost)} / {money(item.estimated_base_cost)} / {money(item.estimated_high_cost)}; **timeline:** {item.remediation_time_months} months")
    disclaimer()

with tabs[2]:
    st.subheader("M&A Deal-Impact Matrix")
    matrix = findings.assign(Finding=findings.finding_id + " — " + findings.title)[["Finding", "risk_rating", "ma_implication", "recommended_timing", "estimated_base_cost", "diligence_question"]]
    matrix.columns = ["Finding", "Cyber Severity", "Deal Impact", "Timing", "Base Remediation", "Diligence Question"]
    for period, description in [("Pre-close", "Issues requiring diligence before completion."), ("Day 1", "Controls required immediately after completion."), ("Day 100", "Priority integration and remediation."), ("6–12 months", "Longer-term transformation activity.")]:
        st.markdown(f"#### {period}"); st.caption(description)
        subset = matrix[matrix.Timing.eq(period)]
        st.dataframe(subset, hide_index=True, width="stretch") if len(subset) else st.write("No items in this period.")
    st.markdown("#### Complete matrix"); st.dataframe(matrix, hide_index=True, width="stretch")
    export("Download M&A Impact Matrix", matrix, "ma_impact_matrix.csv", "matrix")
    st.markdown("#### Buyer versus seller perspective")
    buyer, seller = st.columns(2)
    buyer.info("**Buyer perspective**\n\nPotential remediation liability, transaction uncertainty, integration dependency, and incremental expenditure.")
    seller.info("**Seller perspective**\n\nOpportunity to remediate, evidence compensating controls, clarify funding, and improve disclosure before diligence completes.")
    disclaimer()

with tabs[3]:
    st.subheader("Illustrative Cyber Valuation Sensitivity")
    st.warning("**Cyber remediation cost does not automatically translate into an equivalent purchase-price adjustment. This POC illustrates potential financial sensitivity only.**")
    a, b, c, d, e = st.columns(5)
    ev = a.number_input("Headline enterprise value", min_value=1.0, value=float(company["enterprise_value"]), step=1_000_000.0)
    ebitda = b.number_input("EBITDA", min_value=0.0, value=float(company["ebitda"]), step=1_000_000.0)
    scenario = c.selectbox("Remediation scenario", ["Low", "Base", "High"], index=1)
    adjustment = d.slider("Adjustment percentage", 0, 100, 50, 25) / 100
    contingency = e.number_input("Contingency multiplier", min_value=0.0, value=1.0, step=.1)
    result = calculate_sensitivity(ev, ebitda, totals[scenario], adjustment, contingency)
    metrics = [("Headline EV", money(ev)), ("EV / EBITDA", multiple(result["ev_ebitda"])), ("Selected remediation", money(result["selected_remediation"])), ("Illustrative adjusted EV", money(result["adjusted_ev"]))]
    for col, (label, value) in zip(st.columns(4), metrics): col.metric(label, value)
    for col, (label, value) in zip(st.columns(3), [("Remediation / EV", ratio(result["remediation_ev"])), ("Remediation / EBITDA", ratio(result["remediation_ebitda"])), ("Adjusted EV / EBITDA", multiple(result["adjusted_ev_ebitda"]))]): col.metric(label, value)
    sensitivity = sensitivity_table(ev, ebitda, totals[scenario], contingency)
    st.markdown("#### Illustrative EV sensitivity"); st.line_chart(sensitivity.set_index("Adjustment percentage")["Illustrative adjusted EV"], x_label="Adjustment percentage", y_label="Illustrative adjusted EV")
    export("Download Valuation Sensitivity", sensitivity, "valuation_sensitivity.csv", "valuation")
    disclaimer()

with tabs[4]:
    st.subheader("Integration / 100-Day Remediation Roadmap")
    spend = roadmap.groupby("Timing", as_index=False)["Estimated cost"].sum()
    left, right = st.columns([2, 1])
    left.dataframe(roadmap, hide_index=True, width="stretch", column_config={"Estimated cost": st.column_config.NumberColumn(format="$%d")})
    right.markdown("#### Base spend by period"); right.bar_chart(spend.set_index("Timing")["Estimated cost"])
    export("Download Remediation Roadmap", roadmap, "remediation_roadmap.csv", "roadmap")
    disclaimer()

with tabs[5]:
    st.subheader("Executive Deal-Team Summary")
    st.markdown(executive_summary(findings, company, totals))
    st.markdown("#### High / Critical management questions")
    st.dataframe(findings[findings.risk_rating.isin(["High", "Critical"])][["finding_id", "title", "risk_rating", "diligence_question"]], hide_index=True, width="stretch")
    st.success("Cybersecurity → M&A → Financial Impact → Management Decision Support")
    disclaimer()

with tabs[6]:
    st.subheader("Explainable Methodology")
    st.markdown("""
#### Cyber risk scoring
Explicit points are assigned for severity × 3, likelihood × 2, business criticality × 2, complexity (0–2), and asset breadth (0–2). Scores map to Low (<12), Medium (12–18), High (19–24), or Critical (25+).
#### Remediation estimates
Low, base, and high values are fictional benchmark assumptions aggregated from the register. Source validation rejects missing required estimates.
#### M&A impact mapping
Rules consider calculated risk, relevance flags, domain, complexity, and timeline. Categories prompt review; they are not transaction conclusions.
#### Valuation sensitivity
Headline EV / EBITDA is EV ÷ EBITDA. Selected remediation is cost case × contingency. Illustrative adjusted EV is headline EV − (adjustment percentage × selected remediation). Zero EBITDA returns N/A.
#### Future AI integration
A future narrative provider could consume validated outputs to draft summaries or questions. It should sit after the deterministic engines. No external AI or API is used.
#### Human review
All outputs require cyber, financial, legal, insurance, and transaction-professional judgment. No output recommends a transaction price.
""")
    disclaimer()
