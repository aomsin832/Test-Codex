"""A small Streamlit dashboard for exploring a fictional cyber risk register."""

from pathlib import Path

import pandas as pd
import streamlit as st


# Keep the data path relative to this file so the app works from any directory.
DATA_FILE = Path(__file__).parent / "data" / "risks.csv"
SEVERITY_ORDER = ["Critical", "High", "Medium", "Low"]


@st.cache_data
def load_risks() -> pd.DataFrame:
    """Load the synthetic register and convert due dates into real dates."""
    risks = pd.read_csv(DATA_FILE)
    risks["Due date"] = pd.to_datetime(risks["Due date"])
    return risks


st.set_page_config(page_title="Cyber Risk Register", page_icon="🛡️", layout="wide")

st.title("🛡️ Cyber Risk Register Dashboard")
st.caption("A beginner-friendly view of fictional cybersecurity risks using synthetic data.")

risks = load_risks()
today = pd.Timestamp.today().normalize()

# Closed risks are not included in open-risk or overdue totals.
open_risks = risks[risks["Status"] != "Closed"]
critical_high = open_risks[open_risks["Severity"].isin(["Critical", "High"])]
overdue = open_risks[open_risks["Due date"] < today]

metric_1, metric_2, metric_3 = st.columns(3)
metric_1.metric("Total open risks", len(open_risks))
metric_2.metric("Critical and High risks", len(critical_high))
metric_3.metric("Overdue risks", len(overdue))

st.divider()
st.subheader("Filter the register")

# "All" makes it easy to return to the complete register.
filter_1, filter_2 = st.columns(2)
with filter_1:
    severity_choice = st.multiselect(
        "Severity",
        options=SEVERITY_ORDER,
        default=SEVERITY_ORDER,
    )
with filter_2:
    status_options = sorted(risks["Status"].unique())
    status_choice = st.multiselect(
        "Status",
        options=status_options,
        default=status_options,
    )

filtered_risks = risks[
    risks["Severity"].isin(severity_choice) & risks["Status"].isin(status_choice)
]

st.subheader("Risk register")
st.caption(f"Showing {len(filtered_risks)} of {len(risks)} risks")
st.dataframe(
    filtered_risks,
    use_container_width=True,
    hide_index=True,
    column_config={"Due date": st.column_config.DateColumn(format="YYYY-MM-DD")},
)

st.subheader("Risks by severity")

# Reindexing keeps the bars in a natural risk order, even after filtering.
severity_counts = (
    filtered_risks["Severity"]
    .value_counts()
    .reindex(SEVERITY_ORDER, fill_value=0)
    .rename("Number of risks")
)
st.bar_chart(severity_counts, x_label="Severity", y_label="Number of risks")

st.caption("All names, organizations, scenarios, and risk records shown here are fictional.")
