# AK Duplicate Artifact Report

## Executive Summary
This report identifies duplicate artifacts in the repository that violate the canonical placement rules and create redundancy. Duplicates increase maintenance burden and risk of inconsistency.

## Duplicate Reports Analysis

### Identified Duplicates in docs/reports/
| Artifact Name | Instances | Locations | Recommended Action |
|---------------|-----------|-----------|-------------------|
| AK_LEGACY_LEARNING_INVENTORY | 2 | docs/reports/AK_LEGACY_LEARNING_INVENTORY.csv, docs/reports/AK_LEGACY_LEARNING_INVENTORY.md | KEEP_CANONICAL (both formats serve different purposes) |

## Analysis of Duplicate Types

### 1. Format Variants (Different Extensions, Same Base Name)
These represent the same logical content in different formats and are generally acceptable:
- **AK_LEGACY_LEARNING_INVENTORY.csv** + **AK_LEGACY_LEARNING_INVENTORY.md**
  - Reason: CSV contains raw data, Markdown contains formatted report/summary
  - Action: **KEEP_CANONICAL** - Both serve different but complementary purposes
  - Note: Consider creating a metadata file explaining the relationship

### 2. Exact Name Duplicates (Same Name, Same Extension)
No instances found in the current scan.

### 3. Near Duplicates (Similar Content, Different Names)
Require manual review but not automatically detected by this scan.

## Detailed Findings

### AK_LEGACY_LEARNING_INVENTORY.csv
- **Size**: 28,903,545 bytes
- **Modified**: 7/06/2026 4:21 PM
- **Content Type**: Raw legacy knowledge inventory data in CSV format

### AK_LEGACY_LEARNING_INVENTORY.md
- **Size**: 1,976 bytes
- **Modified**: 7/06/2026 10:50 PM
- **Content Type**: Formatted report/summary of the legacy learning inventory

## Recommendations

### For Format Variants (CSV + MD pairs):
**Action: KEEP_CANONICAL**
- Rationale: Different formats serve different purposes
- CSV: Raw data for processing, analysis, migration
- MD: Human-readable summary, insights, conclusions
- Both are valid and complementary artifacts

### For Future Prevention:
1. Establish naming conventions for format variants:
   - `[name]_data.csv` + `[name]_report.md`
   - `[name]_raw.csv` + `[name]_summary.md`
2. Create template README files in directories explaining format relationships
3. Consider creating a manifest or index file for related artifact groups

## Verification of Root-Level Duplicates
Confirmed no duplicate reports (*_REPORT.md), audits (*_AUDIT.md), plans (*_PLAN.md), designs (*_DESIGN.md), specs (*_SPEC.md), or reviews (*_REVIEW.md) exist directly in the repository root.

## Conclusion
The repository contains one set of format variants that are legitimately different representations of the same underlying data. These should be retained as they serve complementary purposes. No true duplicates (identical content in multiple locations) were detected in the automated scan.

**Overall Recommendation**: No action required for the identified items as they represent appropriate format variants rather than problematic duplicates.