#!/usr/bin/env python3
"""
Calculate dictionary tokens for Phase 2 of metrics standardization.
"""

from codon_library_v2 import RefinedComputationalDNA, count_tokens
import json

def main():
    # Initialize codon library
    dna = RefinedComputationalDNA()
    
    # Serialize dictionary content exactly as it would be used
    dict_content = []
    
    # Core primitives
    dict_content.append("=== CORE PRIMITIVES ===")
    for symbol, meaning in dna.primitives.items():
        dict_content.append(f"{symbol}: {meaning}")
    
    # Error primitives
    dict_content.append("=== ERROR PRIMITIVES ===")
    for symbol, meaning in dna.error_primitives.items():
        dict_content.append(f"{symbol}: {meaning}")
    
    # All codons with full definitions
    dict_content.append("=== CODON LIBRARY ===")
    for pattern, codon in dna.codons.items():
        dict_content.append(f"{pattern}: {codon.name} - {codon.precise_meaning}")
        if codon.error_handling:
            dict_content.append(f"  Error: {codon.error_handling}")
    
    # Join and count tokens
    dictionary_text = "\n".join(dict_content)
    dictionary_tokens = count_tokens(dictionary_text)
    
    print(f"Dictionary Tokens (D): {dictionary_tokens}")
    print(f"Total Codons: {len(dna.codons)}")
    print(f"Dictionary Version: v2.0-2025-07-18")
    print(f"Tokenizer: cl100k_base (GPT-4)")
    
    # Save dictionary content for reference
    with open("dictionary_content_v2.txt", "w") as f:
        f.write(dictionary_text)
    
    print(f"\nDictionary content saved to dictionary_content_v2.txt")
    print(f"Dictionary size: {len(dictionary_text)} characters")

if __name__ == "__main__":
    main()