# Senior-manager Cyber M&A credibility review

This review assesses the synthetic POC as a transaction-screening aid, not as a cyber risk assessment, valuation opinion, legal analysis, or investment recommendation. Rankings reflect the risk that the POC could mislead a deal team.

## Critical

### Technical observations were converted directly into deal-breaker and price language (fixed)

The prior rules labelled every calculated Critical item a “Deal-breaker / escalation consideration” and “Purchase-price consideration.” A control gap rarely determines deal treatment without validating scope, exploitability, incidents, regulatory or contractual exposure, existing budgets, buyer overlap, and available protections. The mapping now calls for additional diligence or specialist escalation and uses qualified legal, contract, insurance, integration, and cost-review prompts. The executive summary explicitly states that no single observation supports a deal-breaker or valuation conclusion.

## High

### Pre-close and Day 1 were presented as remediation completion dates (fixed)

The prior roadmap placed Critical observations in “Pre-close” and other flagged observations in “Day 1,” even where source delivery estimates were 6–12 months. In a transaction, these milestones more often mean evidence validation, risk acceptance, a condition/covenant decision, or an interim safeguard. The roadmap now describes the next transaction action and separately displays estimated full-remediation months. The unsupported ERP estimate was also extended to 18 months.

### Severity looked more certain than the evidence supported (fixed)

Several sparse descriptions asserted complete control failure and were assigned Critical severity. MFA, unsupported ERP, encryption, patching, logging, resilience, vendor, and exercise observations now identify what is reported, sampled, or not evidenced and what remains unverified. MFA, ERP, and encryption were reduced from Critical to High pending corroboration; the vendor-governance observation was reduced from High to Medium. This avoids treating absence of evidence as evidence of total control failure.

### Remediation complexity inflated cyber exposure (fixed)

The former score added points when remediation was difficult. Complexity affects execution risk and cost, not the likelihood or impact of the underlying cyber event. It has been removed from the preliminary exposure score and retained in integration/cost planning.

### Generic diligence questions would not support confirmatory diligence (fixed)

Most observations previously received the same request for a funded plan, date, owner, and compensating control. Questions are now domain-specific and seek populations, architecture/exposure, test results, exceptions, incidents, contracts, jurisdictions, recovery evidence, and buyer integration dependencies. These are still prompts; a live diligence request list would need to be tailored to the target and deal perimeter.

## Medium

### Remediation estimates appeared too authoritative (fixed in language and selected assumptions)

Portfolio totals were displayed without enough distinction between a directional benchmark, vendor quote, target budget, accounting provision, and incremental buyer cost. Labels now call the figures unvalidated estimates, benchmark assumptions include scope/procurement caveats, and selected estimates and delivery periods were recalibrated. The valuation view defaults to zero assumed allocation rather than implying a 50% adjustment.

### Domain alone triggered SPA and insurance conclusions (fixed)

The former mapping inferred an SPA consideration for every data-protection or third-party item and an insurance consideration for every security-operations or data-protection item. The revised mapping requests legal/privacy, contract/concentration, or incident/insurance evidence review. Actual treatment depends on breach history, policy wording, disclosure, applicable law, materiality, and negotiation.

### Overall “Severe” deal risk was overly absolute (fixed)

Counting calculated Critical observations is not sufficient to characterize the whole transaction. The headline is now a “diligence priority,” and the narrative distinguishes preliminary exposure from residual risk and transaction outcome.

### Asset counts can create false precision (partly mitigated)

The screening score still uses reported asset breadth because the POC structure includes it, but asset counts are a crude proxy: one identity provider or ERP can matter more than dozens of low-value servers. Explanations now say “reported breadth,” and the score is expressly preliminary. A future methodology revision should use exposure paths, data/service criticality, and control effectiveness, but that would be a feature change and is out of scope here.

### Likelihood remains an unvalidated input (partly mitigated)

The POC has no threat intelligence, exploitability, control-effectiveness, or incident evidence sufficient to substantiate likelihood. The UI and rating explanation now call it “assumed likelihood.” Replacing it with an evidence/confidence model would be a new feature and is intentionally deferred.

## Low

### Terminology mixed findings, risk, severity, and deal impact (fixed where decision-relevant)

Decision-facing labels now use “observation,” “stated technical severity,” “preliminary exposure,” “potential deal relevance,” and “diligence priority.” Internal field names remain unchanged to preserve application and export compatibility.

### The roadmap omitted a Day 30 section (fixed)

The period existed in filters and rules but was absent from the deal-impact display. It is now shown, including an explicit empty state when no synthetic observation maps to it.

## Residual limitations

The POC remains deliberately deterministic and synthetic. It does not model evidence confidence, deal perimeter/carve-out dependencies, control maturity, threat scenarios, loss magnitude, recurring run-rate, existing management budgets, separation costs, synergies, tax/accounting treatment, policy coverage, legal materiality, or negotiated protections. Consequently, its appropriate use is to organize hypotheses, questions, and transaction actions—not to automate residual-risk, valuation, or deal decisions.
