# Alkasik Kingdom Learning Metrics Model

## Purpose

This doctrine defines metrics that answer whether AK is becoming smarter while remaining governed.

Learning improvement means better decisions, safer recommendations, higher reuse, and more mature capabilities. It does not mean autonomous behavior changes.

## Agent-Level Metrics

| Metric | Meaning |
|---|---|
| lesson_quality_average | Average approved lesson quality by agent |
| decision_trace_completion | Percentage of tasks with complete reasoning/evidence/outcome |
| recommendation_acceptance_rate | Share of reviewed recommendations accepted by reviewers |
| repeated_error_reduction | Reduction of repeated mistakes after lessons |
| approved_skill_usage | Count of approved skills referenced in reports |
| quarantine_rate | Share of submitted records quarantined |

## System-Level Metrics

| Metric | Meaning |
|---|---|
| approved_lessons_total | Total approved lessons |
| active_skills_total | Total active skills |
| active_capabilities_total | Total active capabilities |
| cross_agent_reuse_rate | Share of approved knowledge reused by agents other than originator |
| governance_block_rate | Rate of unsafe learning promotions blocked |
| review_latency | Time from draft to reviewed/approved/rejected |

## Learning Efficiency Metrics

| Metric | Meaning |
|---|---|
| lesson_to_skill_conversion_rate | Approved lessons producing skill candidates |
| skill_to_capability_conversion_rate | Approved skills producing capability candidates |
| distillation_efficiency | Useful distilled records per review cycle |
| evidence_density | Reviewed traces per promoted skill/capability |

## Reuse Metrics

| Metric | Meaning |
|---|---|
| reuse_count | Number of times a lesson/skill/capability is referenced |
| reuse_success_rate | Reuse instances with positive outcome |
| cross_domain_reuse | Safe reuse across departments |
| stale_knowledge_rate | Records not reused or contradicted over time |

## Capability Growth Metrics

| Metric | Meaning |
|---|---|
| capability_maturity_distribution | Count by M0..M5 maturity |
| capability_confidence_average | Average confidence of approved/active capabilities |
| capability_retirement_rate | Rate of obsolete or unsafe capabilities retired |
| performance_delta_by_capability | Measured improvement linked to capability use |

## Smarter System Score

Deterministic system score:

```text
learning_quality = approved_lesson_quality_average * 0.20
reuse_strength = cross_agent_reuse_rate * 0.20
skill_growth = active_skill_growth_rate * 0.15
capability_growth = active_capability_growth_rate * 0.15
safety_strength = (1 - unsafe_promotion_rate) * 0.20
efficiency = distillation_efficiency * 0.10

ak_learning_score = round(sum, 2)
```

The score is advisory. Governance review remains mandatory for promotion.
