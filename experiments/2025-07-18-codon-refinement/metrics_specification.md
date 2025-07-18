# Formal Metrics Specification for Computational DNA Research

**Date:** July 18, 2025  
**Version:** 1.0  
**Purpose:** Standardize all compression and fidelity measurements across experiments

## Canonical Metrics Glossary

| Symbol | Metric Name | Formula | Inputs | Edge Cases |
|--------|-------------|---------|--------|------------|
| O | Original Tokens | Direct count | Source code tokenized | Include all whitespace, comments |
| C | Compressed Tokens | Direct count | Codon representation tokenized | Exclude dictionary if separate |
| D | Dictionary Tokens | Direct count | Symbol table tokenized | One-time overhead cost |
| k | Amortization Factor | Usage count | Number of times dictionary used | k=1 for single use, k=total_tests for full amortization |
| GCR | Gross Compression Ratio | 1 - (C / O) | O, C | Can be negative if C > O |
| NCR | Net Compression Ratio | 1 - ((C + D/k) / O) | O, C, D, k | Accounts for dictionary overhead |
| SFS | Semantic Fidelity Score | (Compressed Accuracy / Baseline Accuracy) * 100 | Baseline correct count, Compressed correct count | N/A if baseline cannot be established |
| RTR | Round-Trip Recoverability | (Recovered Semantic Units / Total Semantic Units) * 100 | Semantic unit counts by type | Requires explicit unit taxonomy |
| ECS | Error Coverage Score | (Recovered Error Paths / Total Error Paths) * 100 | Error path counts | N/A if no error paths in original |
| CEI | Compression Efficiency Index | NCR(k_default) * (SFS / 100) | NCR, SFS | Diagnostic only - never use alone for pass/fail |

## Raw Data Schema

Each test record must capture these fields in JSON format:

```json
{
  "test_id": "string (e.g., T1, T2, T7)",
  "date": "ISO date string",
  "pattern_sequence": "string description of code pattern",
  "O": "integer - original tokens",
  "C": "integer - compressed tokens", 
  "D": "integer - dictionary tokens",
  "dict_version": "string - dictionary version tag",
  "k": "integer - amortization factor used",
  "baseline_questions": "array of baseline test questions/assertions",
  "baseline_correct": "integer - correct baseline answers",
  "compressed_correct": "integer - correct compressed answers",
  "semantic_units_total": "integer - total semantic units identified",
  "semantic_units_recovered": "integer - semantic units recoverable from compressed",
  "error_paths_total": "integer - total error handling paths",
  "error_paths_recovered": "integer - error paths recoverable from compressed",
  "notes": "string - additional observations"
}
```

## Semantic Unit Taxonomy

For RTR calculation, count these explicit units:
- **flow_step**: Individual execution steps/operations
- **condition**: Conditional logic branches  
- **assignment**: Variable assignments and state changes
- **context_scope**: Scope boundaries and variable contexts
- **error_path**: Exception handling and error propagation paths

## RTR Algorithm Description

### Phase 4 Implementation

**Semantic Unit Parser:**
1. Analyze test pattern and baseline questions
2. Extract semantic units according to taxonomy
3. Classify each unit by type and error relationship
4. Store in semantic_original/Txx.json

**Reconstruction Simulator:**
1. Load original semantic units
2. Simulate reconstruction from compressed + dictionary
3. Apply pattern-specific recovery confidence scoring
4. Determine recoverability based on codon pattern analysis
5. Store results in semantic_reconstructed/Txx.json

**RTR & ECS Calculation:**
- RTR = (Recovered Semantic Units / Total Semantic Units) * 100
- ECS = (Recovered Error Paths / Total Error Paths) * 100
- Integrity checks: Sr <= Su, Er <= Ep

**Deterministic Approach:**
- No estimates used - all percentages derived from code analysis
- Parser and reconstruction logic produce consistent results
- Same inputs always produce same outputs

## Operating Principles (Prime Directives)

1. **Scope Lock**: Only work on metrics standardization & reanalysis. No new primitives, scaling experiments, model comparisons, or representation changes.

2. **Terminology Consistency**: Use exactly the canonical metric names from the Glossary. No synonyms or alternative terms.

3. **Auditability**: Every derived metric must have its raw inputs captured in JSON before computation.

4. **No Placeholder Work**: If required data is missing, surface a BLOCKER REPORT - do not fabricate values.

5. **Proposal Gate**: Before creating/modifying files beyond approved list, write "PROPOSE:" block and wait for APPROVED:<task_id> token.

## Core Metrics Definitions

### Gross Compression Ratio (GCR)
```
GCR = 1 - (C / O)
```
Where C = Compressed Tokens, O = Original Tokens

### Net Compression Ratio (NCR)
```
NCR(k) = 1 - ((C + D/k) / O)
```
Where D = Dictionary Tokens, k = Amortization Factor

### Semantic Fidelity Score (SFS)
```
SFS = (Compressed Accuracy / Baseline Accuracy) * 100
```
Based on task performance comparison between original and compressed representations.

### Round-Trip Recoverability (RTR)
```
RTR = (Recovered Semantic Units / Total Semantic Units) * 100
```
Using explicit semantic unit taxonomy defined above.

### Error Coverage Score (ECS)
```
ECS = (Recovered Error Paths / Total Error Paths) * 100
```
Measures preservation of error handling semantics.

## Standardized Reporting Format

### Experiment Results Template
```
Pattern: [codon pattern]
Original Tokens: [count]
Compressed Tokens: [count]
Dictionary Tokens: [count] (amortized over [N] uses)

Compression Ratio: [X]% 
Net Compression Ratio: [Y]%
Semantic Fidelity Score: [Z]%
Round-Trip Recoverability: [W]%

Classification: [Lossless/Functional/Lossy/Minimal]
```

### Classification Thresholds

**Excellent**
- NCR(k_tests) ≥ 65% AND SFS ≥ 95% AND RTR ≥ 90%

**Good** 
- NCR(k_tests) ≥ 50% AND SFS ≥ 80% AND RTR ≥ 75%

**Poor**
- Otherwise OR ECS < 60% (if error paths exist)

## Token Counting Standards

### Tokenizer
- **Primary:** cl100k_base (GPT-4 tokenizer)
- **Secondary:** For cross-model validation, report results for each model's tokenizer
- **Method:** Use tiktoken library for consistent counting

### What to Count
**Original Tokens:**
- Complete source code including whitespace, comments, syntax
- No preprocessing or minification

**Compressed Tokens:**
- Codon representation only
- Context headers (if used)
- Symbol definitions (if inline)

**Dictionary Tokens:**
- Symbol table definitions
- Context mappings
- Pattern libraries
- One-time setup cost

## Error Handling in Metrics

### Token Inflation (CR < 0)
When compressed representation uses more tokens than original:
- Report as negative compression: "CR = -15% (15% token inflation)"
- Investigate causes: verbose metadata, redundant encoding, poor pattern matching

### Missing Baselines
When baseline accuracy cannot be established:
- Report SFS as "N/A - baseline not established"
- Document why baseline measurement failed
- Provide alternative fidelity measures if possible

### Incomplete Recovery
When round-trip recovery cannot be measured:
- Report RTR as "N/A - recovery not testable"
- Document what prevents recovery measurement
- Estimate based on available semantic elements

## Validation Requirements

### Before Reporting Results
1. **Token counts verified** using standardized tokenizer
2. **Dictionary overhead calculated** and amortized appropriately
3. **Baseline accuracy established** through independent measurement
4. **Recovery attempt documented** with specific semantic elements tested

### Cross-Experiment Consistency
- Use identical tokenizer and counting method
- Apply same task accuracy measurement protocol
- Document any deviations from standard metrics
- Provide conversion factors when comparing to legacy results

## Legacy Results Conversion

### Existing Compression Claims
Many existing results report "compression" inconsistently. Convert using:

**If reported as "X% compression":**
- Verify definition: does this mean CR = X% or size = X%?
- Standardize to CR format

**If reported as "X% reduction":**
- Convert: CR = X% (reduction = compression in our standard)

**If reported as "compressed to X% of original":**
- Convert: CR = 1 - (X/100)

### Reanalysis Priority
High-priority experiments to reanalyze with standardized metrics:
1. July 2024 validation results (85.7% success rate claim)
2. Token efficiency experiments (30-45% compression claims)
3. Scaling analysis (stable compression at scale)
4. Real-world Rust code analysis (69.85% compression claim)

## METRICS_ACTIVITY_LOG

- 2025-07-18 Phase 1: Added Canonical Metrics Glossary with 10 standardized metrics
- 2025-07-18 Phase 1: Added Raw Data Schema JSON specification  
- 2025-07-18 Phase 1: Added Semantic Unit Taxonomy (5 unit types)
- 2025-07-18 Phase 1: Added Operating Principles (Prime Directives)
- 2025-07-18 Phase 1: Updated core definitions to use canonical terminology (GCR, NCR, SFS, RTR, ECS)
- 2025-07-18 Phase 1: Updated classification thresholds to canonical format
- 2025-07-18 Phase 2: Created baseline_items JSON files for all 7 test cases (T1-T7)
- 2025-07-18 Phase 2: Calculated Dictionary Tokens (D) = 436 using codon_library_v2.py
- 2025-07-18 Phase 2: Updated all baseline JSON files with O, C, D values and metadata
- 2025-07-18 Phase 2: Documented tokenizer (cl100k_base) and dictionary version (v2.0-2025-07-18)
- 2025-07-18 Phase 2 Hardening: Split dictionary into minimal (D_min=107) vs full (D_full=436)
- 2025-07-18 Phase 2 Hardening: Normalized all baseline JSONs with full schema compliance
- 2025-07-18 Phase 2 Hardening: Created TestID mapping table scaffold with cross-references
- 2025-07-18 Phase 2 Hardening: Removed AI Score references from evaluation-facing artifacts
- 2025-07-18 Phase 2 Hardening: Produced baseline_integrity_report.md (all 7 tests compliant)
- 2025-07-18 Phase 2 Hardening: Produced dictionary_table.md (minimal vs full metrics)
- 2025-07-18 Phase 2 Corrections: Added dict_mode, k_single, k_batch, dictionary_hash to all baseline JSONs
- 2025-07-18 Phase 2 Corrections: Generated SHA256 hashes for dictionaries (minimal: 8c1f63e2...)
- 2025-07-18 Phase 2 Corrections: Added minimal dictionary format example (core primitives + codon names only)
- 2025-07-18 Phase 3: Created data_records directory for derived metrics
- 2025-07-18 Phase 3: Computed GCR, NCR_k1, NCR_k7 metrics for all test cases
- 2025-07-18 Phase 3: Generated individual derived_*.json files for each test
- 2025-07-18 Phase 3: Produced ncr_results_phase3.md with tables and analysis
- 2025-07-18 Phase 3: Calculated both simple and size-weighted mean metrics
- 2025-07-18 Phase 4: Created tools directory with semantic unit parser and reconstruction simulator
- 2025-07-18 Phase 4: Implemented deterministic RTR & ECS calculation pipeline
- 2025-07-18 Phase 4: Generated semantic_original and semantic_reconstructed JSON files for all tests
- 2025-07-18 Phase 4: Produced rtr_records/Txx.json with Su, Sr, Ep, Er counts for each test
- 2025-07-18 Phase 4: Created rtr_results_phase4.md with comprehensive RTR & ECS analysis
- 2025-07-18 Phase 4: Verified integrity checks (Sr <= Su, Er <= Ep) for all test records

---

**Status:** Phase 1 Complete - Specification Hardening  
**Next Step:** Phase 2 - Data Acquisition Foundations