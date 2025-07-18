#!/usr/bin/env python3
"""
Phase 2 Hardening: Split dictionary into minimal vs full and recompute D_min.
"""

from codon_library_v2 import RefinedComputationalDNA, count_tokens
import json

def create_minimal_dictionary(dna):
    """Create minimal dictionary with only essential codon mappings."""
    minimal_content = []
    
    # Only core primitives (essential for decoding)
    for symbol, meaning in dna.primitives.items():
        minimal_content.append(f"{symbol}: {meaning.split(' - ')[0]}")  # Just the core meaning
    
    # Only error primitives (essential for decoding)
    for symbol, meaning in dna.error_primitives.items():
        minimal_content.append(f"{symbol}: {meaning.split(' - ')[0]}")
    
    # Only codon patterns and names (no verbose descriptions)
    for pattern, codon in dna.codons.items():
        minimal_content.append(f"{pattern}: {codon.name}")
    
    return "\n".join(minimal_content)

def create_full_dictionary(dna):
    """Create full dictionary with complete definitions."""
    full_content = []
    
    # Complete primitives with full descriptions
    full_content.append("=== CORE PRIMITIVES ===")
    for symbol, meaning in dna.primitives.items():
        full_content.append(f"{symbol}: {meaning}")
    
    # Complete error primitives
    full_content.append("=== ERROR PRIMITIVES ===")
    for symbol, meaning in dna.error_primitives.items():
        full_content.append(f"{symbol}: {meaning}")
    
    # Complete codons with full definitions
    full_content.append("=== CODON LIBRARY ===")
    for pattern, codon in dna.codons.items():
        full_content.append(f"{pattern}: {codon.name} - {codon.precise_meaning}")
        if codon.error_handling:
            full_content.append(f"  Error: {codon.error_handling}")
    
    return "\n".join(full_content)

def main():
    print("=== Phase 2 Hardening: Dictionary Analysis ===")
    
    # Initialize codon library
    dna = RefinedComputationalDNA()
    
    # Create minimal and full dictionaries
    minimal_dict = create_minimal_dictionary(dna)
    full_dict = create_full_dictionary(dna)
    
    # Count tokens for both
    d_min = count_tokens(minimal_dict)
    d_full = count_tokens(full_dict)
    
    print(f"Minimal Dictionary Tokens (D_min): {d_min}")
    print(f"Full Dictionary Tokens (D_full): {d_full}")
    print(f"Dictionary Overhead Ratio: {d_full/d_min:.2f}x")
    print(f"Tokenizer: cl100k_base (GPT-4)")
    
    # Save both dictionaries
    with open("dictionary_minimal_v2.txt", "w") as f:
        f.write(minimal_dict)
    
    with open("dictionary_full_v2.txt", "w") as f:
        f.write(full_dict)
    
    # Create dictionary comparison data
    dict_comparison = {
        "version": "v2.0-2025-07-18",
        "tokenizer": "cl100k_base",
        "minimal": {
            "tokens": d_min,
            "content_length": len(minimal_dict),
            "description": "Essential codon mappings only"
        },
        "full": {
            "tokens": d_full,
            "content_length": len(full_dict),
            "description": "Complete definitions with error handling"
        },
        "overhead_ratio": round(d_full/d_min, 2)
    }
    
    with open("dictionary_comparison.json", "w") as f:
        json.dump(dict_comparison, f, indent=2)
    
    print(f"\nDictionary files saved:")
    print(f"- dictionary_minimal_v2.txt ({d_min} tokens)")
    print(f"- dictionary_full_v2.txt ({d_full} tokens)")
    print(f"- dictionary_comparison.json")

if __name__ == "__main__":
    main()