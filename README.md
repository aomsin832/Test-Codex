# Cyber M&A Due Diligence & Valuation Impact Navigator

A polished, lightweight Streamlit proof of concept that translates synthetic cyber due-diligence findings into explainable risk, remediation requirements, transaction implications, integration priorities, and **illustrative** valuation sensitivity.

> **Synthetic Deal — Demonstration Only. Human review required. POC output is illustrative only.**

## Project purpose and business use case

Cyber M&A diligence often produces technical observations that a deal team must interpret in the context of diligence scope, decision-making, remediation funding, Day-1 readiness, integration, contracts, insurance, and valuation discussions. This POC demonstrates that translation for fictional **Project Atlas**, the acquisition of fictional Atlas Digital Services by fictional NorthStar Capital Partners.

The app does not determine a purchase price, make an investment recommendation, or replace cyber, legal, financial, insurance, or transaction expertise.

## Five-minute demonstration

1. Review fictional transaction metrics and overall deal risk.
2. Filter 14 synthetic findings and inspect the transparent rating explanation.
3. Review low/base/high remediation estimates and domain charts.
4. Show deal implications, timing, and management questions.
5. Review Pre-close, Day 1, Day 30, Day 100, and 6–12 month priorities.
6. Change valuation inputs, remediation case, adjustment percentage, and contingency.
7. Export registers and finish with the deterministic executive summary.

**Cybersecurity → M&A → Financial Impact → Management Decision Support**

## Architecture

```text
Synthetic CSV / JSON
        ↓
Cyber Risk Engine → Remediation Engine → M&A Impact Engine
        ↓                    ↓
Summary Engine       Valuation Sensitivity Engine
        └────────── Streamlit Dashboard ──────────┘
```

Business logic is independent of Streamlit and contains no random or hidden scoring. There is no database, authentication, external service, paid API, API key, or AI call.

## Repository structure

```text
.
├── app.py                         # UI, navigation, charts, filters, exports
├── data/
│   ├── target_company.json        # Fictional Project Atlas transaction
│   ├── cyber_findings.csv         # 14 synthetic findings and estimates
│   └── remediation_benchmarks.csv # Illustrative assumptions
├── src/
│   ├── risk_engine.py             # Transparent point-based cyber scoring
│   ├── remediation_engine.py      # Portfolio totals and roadmap timing
│   ├── deal_impact_engine.py      # M&A mappings and diligence questions
│   ├── valuation_engine.py        # Ratios and illustrative EV sensitivity
│   ├── summary_engine.py          # Deterministic executive narrative
│   └── data_validation.py         # Input validation
├── tests/                         # Unit and end-to-end tests
└── .github/workflows/tests.yml    # Push, PR, and daily checks
```

## How the logic works

### Cyber risk

`src/risk_engine.py` weights inherent severity, likelihood, business criticality, affected-asset breadth, and remediation complexity. Thresholds deterministically map the result to Low, Medium, High, or Critical, and an explanation exposes all drivers.

### Remediation and roadmap

`src/remediation_engine.py` sums source low/base/high estimates rather than hard-coding portfolio totals. Relevance flags, calculated risk, and months determine Pre-close, Day 1, Day 30, Day 100, or 6–12 month placement.

### Deal impact

`src/deal_impact_engine.py` uses risk, domain, relevance, complexity, and timeline rules to attach one or more transaction considerations and a deterministic management question. These are review prompts, not legal or financial conclusions.

### Illustrative valuation sensitivity

`src/valuation_engine.py` calculates:

- headline multiple = enterprise value ÷ EBITDA;
- selected remediation = low/base/high portfolio cost × contingency multiplier;
- remediation / EV and remediation / EBITDA;
- illustrative adjusted EV = headline EV − (selected percentage × selected remediation);
- illustrative adjusted EV / EBITDA.

Zero EBITDA produces `N/A`, not a division error. The percentage is bounded to 0–100%. Remediation cost does **not** automatically equal a purchase-price adjustment.

### Validation

`src/data_validation.py` checks positive EV and EBITDA for source transaction data, required values, unique IDs, enumerations, non-negative costs/assets, and low ≤ base ≤ high. `src/valuation_engine.py` validates interactive financial inputs.

## Setup

Python 3.10+ is recommended.

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Then:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Testing

```bash
pytest
python -m compileall -q app.py src tests
```

The tests cover known valuation examples, zero EBITDA, invalid inputs, risk classifications and explanations, remediation totals/timing, deal mappings, diligence questions, duplicate IDs, missing data, invalid costs/severity, and the full synthetic dataset.

## Future AI integration

A future optional narrative adapter could consume validated engine outputs to draft summaries, questions, explanations, or buyer/seller perspectives. It should be placed after the deterministic engines. Risk scoring, remediation aggregation, validation, and financial calculations must remain deterministic, authoritative, and testable. This version has no AI provider or external API.

## Assumptions and limitations

- Every company, transaction, financial value, incident reference, finding, and benchmark is fictional.
- Estimates are directional synthetic inputs, not vendor quotes or a funded implementation plan.
- Rules are deliberately simple and are not a claim about a universal Cyber M&A methodology.
- Impacts do not incorporate tax, accounting, working capital, debt-like items, synergies, insurance terms, regulatory analysis, or probability-weighted loss.
- CSV downloads reflect the current calculated register; the findings export reflects active filters.
- Streamlit widgets are bounded to prevent negative interactive values, but professional review remains essential.

## Disclaimer

This POC uses synthetic data and is illustrative only. It is not investment advice, a professional valuation, a purchase-price recommendation, or a real cyber due-diligence opinion. It does not replace professional cyber, financial, legal, insurance, tax, accounting, or M&A judgment. **Human review required.**
