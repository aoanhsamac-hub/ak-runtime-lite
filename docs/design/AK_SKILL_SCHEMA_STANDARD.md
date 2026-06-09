# AK Skill Schema Standard v1.0

## Overview

The AK Skill Schema Standard defines the required structure, fields, and validation rules for all skills registered in the National Skill Registry.

## Schema Fields

| # | Field | Type | Required | Default | Description |
|---|-------|------|----------|---------|-------------|
| 1 | skill_id | string | auto-generated | `SKILL-{uuid}` | Unique identifier |
| 2 | name | string | YES | - | Human-readable skill name |
| 3 | version | int | auto | 1 | Version number, incremented on each change |
| 4 | owner_agent | string | YES | - | Agent who owns this skill (OWNER) |
| 5 | primary_users | list[string] | NO | [] | Agents with primary access (PRIMARY_USER) |
| 6 | secondary_users | list[string] | NO | [] | Agents with secondary access (SECONDARY_USER) |
| 7 | forbidden_users | list[string] | NO | [] | Agents blocked from access (FORBIDDEN_USER) |
| 8 | description | string | YES | - | Detailed description of the skill |
| 9 | category | string | YES | "core" | Skill category: core, imported, internal, deprecated, retired |
| 10 | source | string | YES | "internal" | Origin: hermes, opencode, internal, legacy, discovered |
| 11 | status | string | auto | "DRAFT" | Internal status (DRAFT, REVIEWED, APPROVED, ACTIVE, DEPRECATED, SUSPENDED, RETIRED) |
| 12 | lifecycle_stage | string | auto | "PROPOSED" | 10-stage lifecycle (PROPOSED through ARCHIVED) |
| 13 | created_at | string | auto-generated | ISO timestamp | Creation timestamp |
| 14 | updated_at | string | auto-generated | Same as created_at | Last modification timestamp |
| 15 | dependencies | list[string] | NO | [] | Skill IDs this skill depends on |
| 16 | required_tools | list[string] | NO | [] | Tools required to execute this skill |
| 17 | risk_level | string | YES | - | Risk classification |
| 18 | governance_requirements | dict | NO | {} | Governance compliance specifications |
| 19 | validation_requirements | dict | NO | {} | Validation specifications |
| 20 | performance_metrics | dict | NO | {} | Performance measurement specifications |
| 21 | retirement_conditions | dict | NO | {} | Conditions that trigger retirement |
| 22 | stop_conditions | dict | NO | {} | Conditions that trigger immediate stop |
| 23 | audit_requirements | dict | NO | {} | Audit trail specifications |
| 24 | source_lessons | list[string] | YES | - | Lesson IDs that produced this skill |
| 25 | allowed_agents | list[string] | auto | Derived | Union of primary_users + secondary_users |
| 26 | reviewer_agent | string | auto | Same as owner | Agent responsible for review |
| 27 | source_hash | string | auto-generated | SHA-256 | Cryptographic hash of source |
| 28 | test_cases | list[string] | NO | [] | Test case descriptions |

## Validation Rules

- All required fields must be non-empty
- lifecycle_stage must be one of the 10 defined stages
- category must be one of: core, imported, internal, deprecated, retired
- source must be one of: hermes, opencode, internal, legacy, discovered
- forbidden_users may not overlap with primary_users or secondary_users
- owner_agent may not appear in forbidden_users
- CRITICAL/HIGH risk levels require stop_conditions and retirement_conditions respectively

## Governance Authority

This schema is established under Janus Directive AK-WP35.5-001 and governed by:
- Constitution v1.1
- Agent Law v1.0
- Risk Law v1.0
- Knowledge Governance Decree v1.0
- Retention Governance Decree v1.0
