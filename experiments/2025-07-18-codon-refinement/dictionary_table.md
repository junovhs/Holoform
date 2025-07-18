# Dictionary Metrics Table

**Date:** July 18, 2025  
**Purpose:** Compare minimal vs full dictionary overhead metrics  
**Dictionary Version:** v2.0-2025-07-18  
**Tokenizer:** cl100k_base (GPT-4)

## Dictionary Variants

| Variant | Tokens (D) | Content Length | Description | Use Case |
|---------|------------|----------------|-------------|----------|
| **Minimal** | 107 | 512 chars | Essential codon mappings only | Production compression |
| **Full** | 436 | 2,088 chars | Complete definitions with error handling | Development/debugging |

## Overhead Analysis

| Metric | Minimal Dictionary | Full Dictionary | Ratio |
|--------|-------------------|-----------------|-------|
| **Dictionary Tokens** | 107 | 436 | 4.07x |
| **Overhead per Test (k=1)** | 107 tokens | 436 tokens | 4.07x |
| **Overhead per Test (k=7)** | 15.3 tokens | 62.3 tokens | 4.07x |
| **Content Efficiency** | 4.8 tokens/codon | 48.4 tokens/codon | 10.1x |

## Impact on Net Compression Ratio (NCR)

Using test averages for illustration:
- **Average Original Tokens (O):** 94.7
- **Average Compressed Tokens (C):** 25.1
- **Gross Compression Ratio (GCR):** 73.5%

### Single Use (k=1)
| Dictionary | NCR Formula | NCR Result | Impact vs GCR |
|------------|-------------|------------|---------------|
| **Minimal** | 1 - ((25.1 + 107/1) / 94.7) | -39.5% | -113.0 pp |
| **Full** | 1 - ((25.1 + 436/1) / 94.7) | -387.0% | -460.5 pp |

### Full Amortization (k=7)
| Dictionary | NCR Formula | NCR Result | Impact vs GCR |
|------------|-------------|------------|---------------|
| **Minimal** | 1 - ((25.1 + 107/7) / 94.7) | 57.4% | -16.1 pp |
| **Full** | 1 - ((25.1 + 436/7) / 94.7) | 7.6% | -65.9 pp |

## Key Findings

### Dictionary Overhead is Critical
- **Single use:** Both dictionaries result in negative NCR (token inflation)
- **Amortized use:** Only minimal dictionary maintains reasonable NCR
- **Full dictionary:** Requires significant amortization to be viable

### Minimal Dictionary Advantages
- **4x smaller:** 107 vs 436 tokens
- **Better NCR:** 57.4% vs 7.6% at k=7
- **Production ready:** Sufficient for compression tasks

### Full Dictionary Trade-offs
- **Rich semantics:** Complete error handling definitions
- **Development value:** Better for debugging and analysis
- **High overhead:** Requires k≥20 for positive NCR

## Recommendations

### For Production Use
- **Use minimal dictionary (D=107)**
- **Amortize over multiple tests (k≥7)**
- **Expected NCR: 50-60% range**

### For Development/Research
- **Use full dictionary (D=436) for semantic analysis**
- **Switch to minimal for compression metrics**
- **Document which dictionary was used**

## Files Generated

- `dictionary_minimal_v2.txt` - 107 tokens, production use
- `dictionary_full_v2.txt` - 436 tokens, development use  
- `dictionary_comparison.json` - Structured comparison data

**Status:** Dictionary analysis complete, ready for Phase 3 NCR calculations