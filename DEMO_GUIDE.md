# Presenter Guide: Cyber M&A Deal Impact Navigator

Everything in this POC is synthetic. The suggested wording below is designed for a learning demonstration, not a client presentation or professional opinion.

## 30-second project explanation

> This POC shows how cybersecurity due-diligence observations can be translated into information an M&A deal team can use. It starts with technical evidence, explains the business relevance, identifies the next diligence question, estimates a synthetic remediation range, and connects the issue to transaction planning, financial scale, Day 1 readiness, and integration. It does not decide whether to do a deal or prescribe a purchase-price adjustment.

## Two-minute explanation

### The problem

Cyber diligence often produces technical findings, while an M&A team needs to understand what evidence is missing, why an issue matters to the business, what may need attention before close, what must be ready on Day 1, and what investment or integration work may follow. Technical severity alone does not answer those questions.

### The solution

The Navigator provides a transparent learning flow:

> **Evidence and finding → business relevance → additional diligence → remediation → transaction consideration → integration action → illustrative financial sensitivity**

Four fictional targets demonstrate different profiles: Atlas is balanced, Beacon has a stronger cyber posture, Forge has material legacy-technology dependencies, and Harbor has greater data, vendor, privacy, and contractual uncertainty.

### The architecture

Synthetic JSON and CSV data pass through deterministic modules for validation, preliminary-exposure screening, remediation aggregation and timing, M&A prompts, financial sensitivity, integration roadmapping, and executive summary generation. The same engines run for every target. There is no external API, AI model, database, authentication, or hidden scoring.

### The M&A relevance

The output can organize evidence requests, management interviews, specialist validation, Day 1 safeguards, integration budgets, legal or insurance review, and post-close work. A synthetic remediation estimate can show financial scale, but it is not economic loss and does not automatically become a valuation or price adjustment.

## Five-minute demo script

The application opens with **Project Atlas** and sensible defaults. Do not enter data before the demo.

### 0:00–0:30 · Overview

**Page:** `Overview`  
**Click:** Nothing.

Point to the buyer and target, then the metric cards.

Say:

> This is a fictional $250.0 million Enterprise Value acquisition with $20.0 million EBITDA, implying a 12.5x headline EV / EBITDA multiple. The cyber review records 14 observations and a $6.32 million Base synthetic remediation case. The POC is showing how those observations translate into diligence and integration priorities—not whether the acquisition should proceed.

Finish on the four-stage line: **Pre-close evidence → Day 1 readiness → First 100 days → Longer-term transformation**.

### 0:30–1:15 · Cyber Findings

**Page:** `Cyber Findings`  
**Click:** Nothing; use the first priority observation, `F-001 · MFA not enforced for all privileged accounts`.

Say:

> The observation is not treated as a proven enterprise-wide failure. Management reports a subset of privileged accounts without MFA, so the first task is to validate the population, bypass paths, compensating controls, and incident history. Its transaction relevance depends on evidence and business context, not the technical label alone.

Point to the preliminary exposure, business rationale, $0.3 million Base estimate, and two-month delivery estimate.

### 1:15–2:00 · Cyber → M&A

**Page:** `Cyber → M&A`  
**Click:** Leave the default finding `F-001` selected.

Move left-to-right through the four headings:

1. Cyber observation
2. Business implication
3. Transaction consideration
4. Recommended diligence question

Say:

> The buyer question is specific: how many and what percentage of privileged accounts are affected, which paths bypass MFA, what compensating controls operate, and whether related misuse occurred. Possible responses include further diligence, a Day 1 safeguard, and integration planning. None is an automatic deal conclusion.

Briefly contrast the buyer's need for corroboration with the seller's opportunity to provide evidence, demonstrate controls, and clarify funded plans.

### 2:00–2:45 · Remediation

**Page:** `Remediation`  
**Click:** Nothing.

Mention the Atlas portfolio cases:

- Low: **$3.15 million**
- Base: **$6.32 million**
- High: **$11.11 million**

Say:

> These are synthetic planning assumptions, not quotes or provisions. The important distinction is between transaction timing and full technical delivery. An issue may need evidence or an interim safeguard before close even if complete remediation takes 9 or 18 months.

Point to cost by domain, full delivery horizon, and complexity. Do not add cost references across roadmap stages.

### 2:45–3:30 · Financial Sensitivity

**Page:** `Financial Sensitivity`  
**Click:** Keep `Base`, planning factor `1.0`, and first show allocation `0%`. Then move **Hypothetical allocation (%)** to `50%`.

At 0%, point out:

- Headline EV / EBITDA: **12.5x**
- Selected synthetic remediation cost: **$6.3m**
- Cost / EV: **2.5%**
- Cost / EBITDA: **31.6%**
- Illustrative EV: **$250.0m**

At 50%, point out the **$3.2m** hypothetical allocation and **$246.8m** illustrative EV.

Say:

> This is scale arithmetic only. The cost may be capital, operating, recurring, internal, already budgeted, or buyer-specific. It is not automatically economic loss or a purchase-price deduction. Actual treatment depends on evidence, structure, negotiation, accounting, legal analysis, and judgment.

### 3:30–4:15 · Integration Roadmap

**Page:** `Integration Roadmap`  
**Click:** Nothing.

Say:

> The same finding can appear at more than one stage: validate it before close, establish an interim safeguard on Day 1, and complete remediation later. The repeated Base cost is a reference to the same programme, not additional spend at every stage.

Show Pre-close, Day 1, Day 100, and Longer-term transformation. Use the unsupported ERP as the example of a pre-close decision with an 18-month delivery horizon.

### 4:15–5:00 · Target Comparison

**Page:** `Target Comparison`  
**Click:** Nothing initially. The pair defaults to **Atlas Digital Services** and **Harbor Customer Analytics**, whose headline EVs are $250.0m and $275.0m.

Say:

> Similar headline valuations can conceal different cyber profiles. Atlas is a balanced transformation case. Harbor has a lower Base remediation case of $3.28 million, but a greater concentration of data, vendor, privacy, and contractual uncertainty. Forge, by contrast, has the lowest headline EV but the largest remediation requirement relative to EV because of legacy technology. Beacon has the highest headline multiple and the lowest cyber remediation scale. Cyber informs the diligence and integration plan, but it does not rank the investments.

Point to the four profile tables, then the Target A versus Target B investigation questions.

## Common questions

### What does the tool actually calculate?

It calculates a transparent preliminary-exposure screen, Low/Base/High synthetic remediation totals, timing groupings, transaction-prompt mappings, EV / EBITDA, cost / EV, cost / EBITDA, hypothetical allocation, illustrative EV, and illustrative EV / EBITDA. It also counts diligence and integration items across targets. It does not calculate risk loss or company value.

### Where do the findings come from?

They are authored synthetic observations stored in CSV files for four fictional targets. They are not scans, client findings, market benchmarks, or outputs from an external service.

### Is this a valuation model?

No. It does not estimate fair value, select a market multiple, forecast cash flow, calculate equity value, or recommend price. The financial page is an illustrative sensitivity showing the scale of a hypothetical allocation assumption.

### Why would a buyer care about cyber findings?

Findings may reveal business disruption, data, contractual, regulatory, incident, continuity, investment, or integration considerations. They also identify uncertainty that the buyer may need to resolve before connecting or operating the business.

### Why doesn't remediation cost equal purchase-price reduction?

Cost is not necessarily economic loss. It may be capital or operating expenditure, already budgeted, recurring, shared with integration, buyer-specific, insured, or avoidable through a different solution. Transaction treatment depends on evidence, negotiation, deal structure, accounting, tax, legal analysis, and competing commercial considerations.

### How is this different from a penetration test?

A penetration test attempts to identify and demonstrate exploitable technical weaknesses in a defined scope. Cyber M&A diligence uses multiple evidence sources to interpret cyber exposure in the context of the business and transaction. A penetration test may be one input, but it does not answer all transaction questions.

### How is this different from a cyber maturity assessment?

A maturity assessment compares capabilities with a framework or target state, often in more depth and over a longer period. M&A diligence is time-bound, evidence-constrained, and focused on material transaction, readiness, and integration questions. The two can overlap but have different objectives.

### Where could AI be added later?

AI could help draft evidence requests, summarize validated outputs, identify similar observations, or tailor learning narratives. It should sit after deterministic validation and calculation, preserve source traceability, and remain subject to human review. This version contains no AI integration.

### What parts require human judgment?

Scoping, evidence reliability, threat relevance, business criticality, legal and regulatory interpretation, insurance response, cost estimation, accounting treatment, materiality, transaction protections, integration feasibility, and any investment or price decision all require qualified people.

## Presenter guardrails

- Say **observation**, **preliminary exposure**, **synthetic cost**, and **transaction consideration**.
- Do not say a target is “worth” the illustrative EV.
- Do not add repeated roadmap cost references across stages.
- Do not compare finding counts without discussing scope and evidence quality.
- Do not imply that cybersecurity is the sole reason to acquire or reject a target.
