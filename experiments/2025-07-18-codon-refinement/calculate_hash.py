#!/usr/bin/env python3
"""
Calculate SHA256 hash for dictionary files.
"""

import hashlib
import json

def calculate_file_hash(filename):
    """Calculate SHA256 hash of a file."""
    with open(filename, 'rb') as f:
        content = f.read()
    return hashlib.sha256(content).hexdigest()

def main():
    # Calculate hashes
    minimal_hash = calculate_file_hash('dictionary_minimal_v2.txt')
    full_hash = calculate_file_hash('dictionary_full_v2.txt')
    
    print(f"Minimal Dictionary SHA256: {minimal_hash}")
    print(f"Full Dictionary SHA256: {full_hash}")
    
    # Save hash information
    hash_info = {
        "minimal_dictionary": {
            "file": "dictionary_minimal_v2.txt",
            "sha256": minimal_hash,
            "tokens": 107
        },
        "full_dictionary": {
            "file": "dictionary_full_v2.txt",
            "sha256": full_hash,
            "tokens": 436
        }
    }
    
    with open('dictionary_hashes.json', 'w') as f:
        json.dump(hash_info, f, indent=2)
    
    print(f"\nHash information saved to dictionary_hashes.json")
    
    # Read minimal dictionary for example
    with open('dictionary_minimal_v2.txt', 'r') as f:
        minimal_content = f.read()
    
    print("\nMinimal Dictionary Format Example (first 200 chars):")
    print("-" * 60)
    print(minimal_content[:200] + "...")
    print("-" * 60)

if __name__ == "__main__":
    main()