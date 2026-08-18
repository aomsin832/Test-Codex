# Cyber M&A Due Diligence & Valuation Impact Navigator

A polished, lightweight Streamlit proof of concept that translates synthetic cyber due-diligence findings into explainable risk, remediation requirements, transaction considerations, integration priorities, and **illustrative financial sensitivity**.

> **Synthetic Deal — Demonstration Only. Human review required. POC output is illustrative only.**

## Project purpose and business use case

Cyber M&A diligence often produces technical observations that a deal team must interpret in the context of diligence scope, decision-making, remediation funding, Day-1 readiness, integration, contracts, insurance, and valuation discussions. This POC demonstrates that translation across four fictional acquisition targets. **Project Atlas** remains the default balanced example; Project Beacon demonstrates a stronger cyber posture, Project Forge demonstrates legacy-technology investment needs, and Project Harbor demonstrates data and third-party diligence uncertainty.

The app does not determine a purchase price, make an investment recommendation, or replace cyber, legal, financial, insurance, or transaction expertise.

The senior-manager credibility assessment, ranked issues, fixes, and deliberately deferred limitations are documented in [`CYBER_MA_REVIEW.md`](CYBER_MA_REVIEW.md).

New to Cyber M&A? Start with [`LEARNING_GUIDE.md`](LEARNING_GUIDE.md), then follow the application from **Overview** through **Executive Summary**.

Presenting the POC? Use [`DEMO_GUIDE.md`](DEMO_GUIDE.md) for a 30-second explanation, two-minute overview, exact five-minute walkthrough, and common questions.

## Five-minute demonstration

1. Review fictional transaction metrics and overall diligence priority.
2. Select one of four synthetic targets, filter its observations, and inspect the transparent preliminary-exposure explanation.
3. Review low/base/high remediation estimates and domain charts.
4. Show deal implications, timing, and management questions.
5. Review Pre-close, Day 1, Day 30, Day 100, and 6–12 month actions, distinguishing transaction decisions and interim safeguards from full remediation delivery.
6. Change financial inputs, synthetic remediation case, hypothetical allocation percentage, and cost planning factor.
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
│   ├── targets/                   # Extensible synthetic target profiles
│   │   ├── atlas/                 # company.json + findings.csv
│   │   ├── beacon/                # Stronger cyber posture
│   │   ├── forge/                 # Legacy technology risk
│   │   └── harbor/                # Data and third-party risk
│   └── remediation_benchmarks.csv # Illustrative assumptions
├── src/
│   ├── risk_engine.py             # Transparent point-based cyber scoring
│   ├── remediation_engine.py      # Portfolio totals and roadmap timing
│   ├── deal_impact_engine.py      # M&A mappings and diligence questions
│   ├── valuation_engine.py        # Ratios and illustrative EV sensitivity
│   ├── summary_engine.py          # Deterministic executive narrative
│   ├── target_engine.py           # Target discovery and comparison metrics
│   └── data_validation.py         # Input validation
├── tests/                         # Unit and end-to-end tests
└── .github/workflows/tests.yml    # Push, PR, and daily checks
```

## How the logic works

### Cyber risk

`src/risk_engine.py` produces a preliminary exposure screen from stated technical severity, assumed likelihood, business criticality, and reported affected-asset breadth. Remediation complexity is deliberately excluded: difficulty and cost do not make an exposure more severe. Thresholds map the result to Low, Medium, High, or Critical, but the output is not a residual-risk opinion and must be validated against evidence, scope, exploitability, and compensating controls.

### Remediation and roadmap

`src/remediation_engine.py` sums source low/base/high estimates rather than hard-coding portfolio totals. Pre-close and Day 1 placement identifies the next diligence decision or interim safeguard, not a commitment to finish remediation by that milestone. A separate delivery-month field retains the estimated full-remediation duration.

### Transaction considerations

`src/deal_impact_engine.py` uses preliminary exposure, domain, relevance, complexity, and timeline rules to attach qualified transaction considerations and evidence-led diligence questions. It routes observations to additional diligence, specialist assessment, readiness, integration, or cost validation rather than calling a technical observation a deal-breaker or automatic price adjustment.

### Illustrative financial sensitivity

`src/valuation_engine.py` calculates:

- headline multiple = enterprise value ÷ EBITDA;
- selected synthetic cost = calculated low/base/high portfolio cost × synthetic planning factor;
- cost / EV and cost / EBITDA scale indicators;
- hypothetical transaction allocation = allocation percentage × selected synthetic cost;
- illustrative EV = headline EV − hypothetical transaction allocation;
- illustrative EV / EBITDA.

Zero EBITDA produces `N/A`, not a division error. The allocation is bounded to 0–100%. Remediation expenditure does **not** automatically equal economic loss or a purchase-price adjustment. It may comprise operating expenditure, capital expenditure, one-time implementation cost, internal resource cost, or recurring cost; the POC does not determine accounting treatment.

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

The tests cover explicit EV/EBITDA, cost/EV, cost/EBITDA, 0%/50%/100% allocation and adjusted-multiple examples; scenario selection; zero EBITDA and remediation; invalid inputs; risk classifications; remediation totals/timing; transaction mappings; validation; and the full synthetic dataset.

## Future AI integration

A future optional narrative adapter could consume validated engine outputs to draft summaries, questions, explanations, or buyer/seller perspectives. It should be placed after the deterministic engines. Risk scoring, remediation aggregation, validation, and financial calculations must remain deterministic, authoritative, and testable. This version has no AI provider or external API.

## Assumptions and limitations

- Every company, transaction, financial value, incident reference, finding, and cost assumption is fictional.
- Estimates are directional synthetic inputs, not vendor quotes, accounting provisions, or a funded implementation plan; buyer operating-model overlap and existing target budgets are not reflected.
- Missing or partial control evidence is not treated as proof that a control is wholly absent or ineffective.
- Pre-close and Day 1 labels identify transaction actions and interim safeguards, while full remediation may take materially longer.
- Rules are deliberately simple and are not a claim about a universal Cyber M&A methodology.
- Impacts do not incorporate tax, accounting, working capital, debt-like items, synergies, insurance terms, regulatory analysis, or probability-weighted loss.
- CSV downloads reflect the current calculated register; the findings export reflects active filters.
- Streamlit widgets are bounded to prevent negative interactive values, but professional review remains essential.

## Disclaimer

This POC uses synthetic data and is illustrative only. It is not investment advice, a professional valuation, a purchase-price recommendation, or a real cyber due-diligence opinion. It does not replace professional cyber, financial, legal, insurance, tax, accounting, or M&A judgment. **Human review required.**
