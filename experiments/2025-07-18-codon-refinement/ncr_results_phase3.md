# NCR Results - Phase 3

**Date:** 2025-07-18  
**Dictionary:** Minimal (D=107 tokens)  
**Dictionary Hash:** 8c1f63e2...  
**Amortization Factors:** k_single=1, k_batch=7

## Metrics Table

| TestID | Pattern | O | C | D | GCR | NCR(k=1) | NCR(k=7) | NCR_full(k=1) | NCR_full(k=7) | Delta(k=1) | Delta(k=7) |
|--------|---------|---|---|---|-----|----------|----------|---------------|---------------|------------|------------|
| T1 | Context Scoping Logi... | 62 | 22 | 107 | 64.5% | -108.1% | 39.9% | -638.7% | -35.9% | -172.6% | -24.7% |
| T2 | Error Recovery Flow ... | 65 | 19 | 107 | 70.8% | -93.8% | 47.3% | -600.0% | -25.1% | -164.6% | -23.5% |
| T3 | Expert CLI Operation... | 184 | 40 | 107 | 78.3% | 20.1% | 70.0% | -158.7% | 44.4% | -58.2% | -8.3% |
| T4 | Multi-Condition Deci... | 94 | 33 | 107 | 64.9% | -48.9% | 48.6% | -398.9% | -1.4% | -113.8% | -16.3% |
| T5 | Resource Management ... | 86 | 24 | 107 | 72.1% | -52.3% | 54.3% | -434.9% | -0.3% | -124.4% | -17.8% |
| T6 | Concurrent Context H... | 122 | 22 | 107 | 82.0% | -5.7% | 69.4% | -275.4% | 30.9% | -87.7% | -12.5% |
| T7 | Basic Git Operation... | 71 | 16 | 107 | 77.5% | -73.2% | 55.9% | -536.6% | -10.3% | -150.7% | -21.5% |


## Aggregate Results

### Simple Mean (Equal Test Weighting)
- **Average GCR:** 72.9%
- **Average NCR(k=1):** -51.7%
- **Average NCR(k=7):** 55.1%
- **Average Delta(k=1):** -124.6%
- **Average Delta(k=7):** -17.8%

### Size-Weighted Mean (By Original Tokens)
- **Weighted GCR:** 74.3%
- **Weighted NCR(k=1):** -35.2%
- **Weighted NCR(k=7):** 58.6%
- **Weighted Delta(k=1):** -109.5%
- **Weighted Delta(k=7):** -15.6%

## Optional: Full Dictionary Comparison

| Metric | Minimal Dictionary | Full Dictionary | Difference |
|--------|-------------------|-----------------|------------|
| NCR(k=1) | -51.7% | -434.8% | 383.0% |
| NCR(k=7) | 55.1% | 0.3% | 54.7% |

## Analysis

### Key Findings
1. **Dictionary Overhead Impact:** The difference between GCR and NCR(k=1) shows significant dictionary overhead for single use.
2. **Batch Amortization Benefit:** NCR(k=7) demonstrates the value of amortizing dictionary costs across multiple tests.
3. **Minimal vs Full Dictionary:** Using the minimal dictionary provides substantial NCR improvements compared to the full dictionary.

### Recommendations
1. **Use Batch Processing:** Always process multiple tests to amortize dictionary overhead.
2. **Prefer Minimal Dictionary:** For production use, the minimal dictionary provides better compression efficiency.
3. **Consider Test Size:** Larger tests (higher O) show better NCR due to fixed dictionary overhead being proportionally smaller.

## Next Steps
- Proceed to Phase 4 - RTR & ECS Harness
- Implement reconstruction logic to measure semantic recovery
- Calculate actual RTR & ECS values for each test

---

**Status:** Phase 3 Complete  
**Next Phase:** Phase 4 - RTR & ECS Harness
