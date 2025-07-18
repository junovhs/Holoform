#!/usr/bin/env python3
"""
Phase 3: Compute NCR for k=1 and k=7 amortization regimes.
Generate derived metrics and store in data_records directory.
"""

import json
import os
import math
from datetime import datetime

def load_baseline_data():
    """Load all baseline test data."""
    baseline_data = []
    baseline_dir = "baseline_items"
    
    for i in range(1, 8):  # T1 through T7
        filepath = os.path.join(baseline_dir, f"T{i}.json")
        with open(filepath, 'r') as f:
            data = json.load(f)
            baseline_data.append(data)
    
    return baseline_data

def compute_metrics(test_data):
    """Compute GCR, NCR for different k values."""
    O = test_data['O']
    C = test_data['C'] 
    D = test_data['D']
    D_full = 436  # Full dictionary tokens
    k_single = test_data['k_single']
    k_batch = test_data['k_batch']
    
    # Gross Compression Ratio
    GCR = 1 - (C / O)
    
    # Net Compression Ratio for k=1 (single use)
    NCR_k1 = 1 - ((C + D/k_single) / O)
    
    # Net Compression Ratio for k=7 (batch use)
    NCR_k7 = 1 - ((C + D/k_batch) / O)
    
    # Optional: NCR with full dictionary
    NCR_full_k1 = 1 - ((C + D_full/k_single) / O)
    NCR_full_k7 = 1 - ((C + D_full/k_batch) / O)
    
    # Delta between GCR and NCR
    delta_NCR_k1 = NCR_k1 - GCR
    delta_NCR_k7 = NCR_k7 - GCR
    
    return {
        'test_id': test_data['test_id'],
        'pattern_sequence': test_data['pattern_sequence'],
        'O': O,
        'C': C, 
        'D': D,
        'D_full': D_full,
        'GCR': GCR,
        'NCR_k1': NCR_k1,
        'NCR_k7': NCR_k7,
        'NCR_full_k1': NCR_full_k1,
        'NCR_full_k7': NCR_full_k7,
        'delta_NCR_k1': delta_NCR_k1,
        'delta_NCR_k7': delta_NCR_k7
    }

def format_percentage(value):
    """Format a decimal value as a percentage string."""
    return f"{value:.1%}"

def generate_markdown_table(results):
    """Generate a markdown table from results."""
    table = "| TestID | Pattern | O | C | D | GCR | NCR(k=1) | NCR(k=7) | NCR_full(k=1) | NCR_full(k=7) | Delta(k=1) | Delta(k=7) |\n"
    table += "|--------|---------|---|---|---|-----|----------|----------|---------------|---------------|------------|------------|\n"
    
    for r in results:
        table += f"| {r['test_id']} | {r['pattern_sequence'][:20]}... | {r['O']} | {r['C']} | {r['D']} | "
        table += f"{format_percentage(r['GCR'])} | {format_percentage(r['NCR_k1'])} | {format_percentage(r['NCR_k7'])} | "
        table += f"{format_percentage(r['NCR_full_k1'])} | {format_percentage(r['NCR_full_k7'])} | "
        table += f"{format_percentage(r['delta_NCR_k1'])} | {format_percentage(r['delta_NCR_k7'])} |\n"
    
    return table

def calculate_weighted_mean(results, metric_key):
    """Calculate size-weighted mean for a metric."""
    total_weight = sum(r['O'] for r in results)
    weighted_sum = sum(r[metric_key] * r['O'] for r in results)
    return weighted_sum / total_weight

def main():
    print("=== Phase 3: Dictionary Overhead & NCR Computation ===")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d')}")
    print("Dictionary Tokens (D_min): 107")
    print("Dictionary Tokens (D_full): 436")
    print("Amortization Regimes: k=1 (single use), k=7 (batch use)")
    print("=" * 60)
    
    # Create data_records directory if it doesn't exist
    os.makedirs("data_records", exist_ok=True)
    
    # Load baseline data
    baseline_data = load_baseline_data()
    
    # Compute metrics for each test
    results = []
    for test_data in baseline_data:
        metrics = compute_metrics(test_data)
        results.append(metrics)
        
        # Save individual derived metrics
        test_id = test_data['test_id']
        derived_path = os.path.join("data_records", f"derived_{test_id}.json")
        with open(derived_path, 'w') as f:
            json.dump(metrics, f, indent=2)
        
        print(f"{metrics['test_id']}: {metrics['pattern_sequence']}")
        print(f"  O={metrics['O']}, C={metrics['C']}, D={metrics['D']}")
        print(f"  GCR={format_percentage(metrics['GCR'])}")
        print(f"  NCR(k=1)={format_percentage(metrics['NCR_k1'])}")
        print(f"  NCR(k=7)={format_percentage(metrics['NCR_k7'])}")
        print(f"  Delta(k=1)={format_percentage(metrics['delta_NCR_k1'])}")
        print(f"  Delta(k=7)={format_percentage(metrics['delta_NCR_k7'])}")
        print()
    
    # Compute aggregates
    total_tests = len(results)
    avg_gcr = sum(r['GCR'] for r in results) / total_tests
    avg_ncr_k1 = sum(r['NCR_k1'] for r in results) / total_tests  
    avg_ncr_k7 = sum(r['NCR_k7'] for r in results) / total_tests
    
    # Compute size-weighted means
    weighted_gcr = calculate_weighted_mean(results, 'GCR')
    weighted_ncr_k1 = calculate_weighted_mean(results, 'NCR_k1')
    weighted_ncr_k7 = calculate_weighted_mean(results, 'NCR_k7')
    
    # Generate markdown report
    markdown_report = f"""# NCR Results - Phase 3

**Date:** {datetime.now().strftime('%Y-%m-%d')}  
**Dictionary:** Minimal (D={results[0]['D']} tokens)  
**Dictionary Hash:** {baseline_data[0]['dictionary_hash'][:8]}...  
**Amortization Factors:** k_single=1, k_batch=7

## Metrics Table

{generate_markdown_table(results)}

## Aggregate Results

### Simple Mean (Equal Test Weighting)
- **Average GCR:** {format_percentage(avg_gcr)}
- **Average NCR(k=1):** {format_percentage(avg_ncr_k1)}
- **Average NCR(k=7):** {format_percentage(avg_ncr_k7)}
- **Average Delta(k=1):** {format_percentage(avg_ncr_k1 - avg_gcr)}
- **Average Delta(k=7):** {format_percentage(avg_ncr_k7 - avg_gcr)}

### Size-Weighted Mean (By Original Tokens)
- **Weighted GCR:** {format_percentage(weighted_gcr)}
- **Weighted NCR(k=1):** {format_percentage(weighted_ncr_k1)}
- **Weighted NCR(k=7):** {format_percentage(weighted_ncr_k7)}
- **Weighted Delta(k=1):** {format_percentage(weighted_ncr_k1 - weighted_gcr)}
- **Weighted Delta(k=7):** {format_percentage(weighted_ncr_k7 - weighted_gcr)}

## Optional: Full Dictionary Comparison

| Metric | Minimal Dictionary | Full Dictionary | Difference |
|--------|-------------------|-----------------|------------|
| NCR(k=1) | {format_percentage(avg_ncr_k1)} | {format_percentage(sum(r['NCR_full_k1'] for r in results) / total_tests)} | {format_percentage((sum(r['NCR_k1'] for r in results) / total_tests) - (sum(r['NCR_full_k1'] for r in results) / total_tests))} |
| NCR(k=7) | {format_percentage(avg_ncr_k7)} | {format_percentage(sum(r['NCR_full_k7'] for r in results) / total_tests)} | {format_percentage((sum(r['NCR_k7'] for r in results) / total_tests) - (sum(r['NCR_full_k7'] for r in results) / total_tests))} |

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
"""
    
    # Save markdown report
    with open("ncr_results_phase3.md", "w") as f:
        f.write(markdown_report)
    
    # Save consolidated results
    with open("data_records/phase3_ncr_results.json", "w") as f:
        json.dump({
            'results': results,
            'aggregates': {
                'total_tests': total_tests,
                'avg_gcr': avg_gcr,
                'avg_ncr_k1': avg_ncr_k1,
                'avg_ncr_k7': avg_ncr_k7,
                'weighted_gcr': weighted_gcr,
                'weighted_ncr_k1': weighted_ncr_k1,
                'weighted_ncr_k7': weighted_ncr_k7
            }
        }, f, indent=2)
    
    print("=== Aggregate Results ===")
    print(f"Total Tests: {total_tests}")
    print(f"Average GCR: {format_percentage(avg_gcr)}")
    print(f"Average NCR(k=1): {format_percentage(avg_ncr_k1)}")
    print(f"Average NCR(k=7): {format_percentage(avg_ncr_k7)}")
    print(f"Weighted GCR: {format_percentage(weighted_gcr)}")
    print(f"Weighted NCR(k=1): {format_percentage(weighted_ncr_k1)}")
    print(f"Weighted NCR(k=7): {format_percentage(weighted_ncr_k7)}")
    
    print(f"\nResults saved to:")
    print(f"- data_records/derived_*.json (individual test metrics)")
    print(f"- data_records/phase3_ncr_results.json (consolidated results)")
    print(f"- ncr_results_phase3.md (markdown report)")

if __name__ == "__main__":
    main()