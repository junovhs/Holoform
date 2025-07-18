# RTR & ECS Results - Phase 4

**Date:** 2025-07-18  
**Methodology:** Deterministic reconstruction simulation  
**Parser:** Semantic unit taxonomy (flow_step, condition, assignment, context_scope, error_path)  
**Simulator:** Pattern-based reconstruction confidence scoring

## Results Table

| TestID | Pattern | Su | Sr | Ep | Er | RTR | ECS |
|--------|---------|----|----|----|----|-----|-----|
| T1 | Context Scoping Logic (In... | 4 | 4 | 0 | 0 | 100.0% | N/A |
| T2 | Error Recovery Flow (Adva... | 4 | 3 | 2 | 2 | 75.0% | 100.0% |
| T3 | Expert CLI Operation... | 5 | 4 | 0 | 0 | 80.0% | N/A |
| T4 | Multi-Condition Decision ... | 4 | 4 | 0 | 0 | 100.0% | N/A |
| T5 | Resource Management (FAIL... | 4 | 1 | 2 | 0 | 25.0% | 0.0% |
| T6 | Concurrent Context Handli... | 4 | 4 | 1 | 1 | 100.0% | 100.0% |
| T7 | Basic Git Operation... | 3 | 3 | 0 | 0 | 100.0% | N/A |


## Aggregate Metrics

### Round-Trip Recoverability (RTR)
- **Average RTR:** 82.9%
- **Best RTR:** 100.0% (T1)
- **Worst RTR:** 25.0% (T5)

### Error Coverage Score (ECS)
- **Average ECS:** 66.7% (across 3 tests with error paths)
- **Tests with Error Paths:** 3/7
- **Error Path Recovery Rate:** 3/5 (60.0%)

## Analysis by Test Pattern

### Excellent Recovery (RTR >= 90%)
- **T1** (100.0%): Context Scoping Logic (Intermediate)
- **T4** (100.0%): Multi-Condition Decision Tree
- **T6** (100.0%): Concurrent Context Handling
- **T7** (100.0%): Basic Git Operation

### Good Recovery (RTR 75-89%)
- **T2** (75.0%): Error Recovery Flow (Advanced)
- **T3** (80.0%): Expert CLI Operation

### Poor Recovery (RTR < 75%)
- **T5** (25.0%): Resource Management (FAILED)


## Error Handling Analysis

### Tests with Error Paths
- **T2**: 2/2 error paths recovered (100.0%)
- **T5**: 0/2 error paths recovered (0.0%)
- **T6**: 1/1 error paths recovered (100.0%)


## Key Findings

### Semantic Unit Recovery Patterns
1. **Context and Flow Operations** show highest recovery rates
2. **Conditional Logic** generally well preserved in codon representations
3. **Assignment Operations** consistently recoverable
4. **Error Handling** shows variable recovery depending on complexity

### Critical Limitations Identified
1. **T5 (Resource Management)**: Significant error handling loss
2. **Complex Error Flows**: Cleanup operations often not recoverable
3. **Multi-step Error Recovery**: Partial information loss in compression

### Validation of Original Claims
- Original validation claims largely supported by RTR analysis
- Tests marked as "PASS" show RTR >= 75%
- T5 "FAILED" status confirmed by poor error path recovery

## Integrity Verification

All RTR records pass integrity checks:
- Sr <= Su (recovered units <= total units): PASS
- Er <= Ep (recovered error paths <= total error paths): PASS

## Methodology Notes

### Deterministic Approach
- No estimates used - all percentages derived from code analysis
- Parser and reconstruction logic produce consistent results
- Reconstruction confidence scores based on codon pattern analysis

### Semantic Unit Taxonomy Applied
- **flow_step**: Individual execution steps/operations
- **condition**: Conditional logic branches
- **assignment**: Variable assignments and state changes
- **context_scope**: Scope boundaries and variable contexts
- **error_path**: Exception handling and error propagation paths

---

**Status:** Phase 4 Complete  
**Next Phase:** Phase 5 - Baseline Accuracy & SFS
