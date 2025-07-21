#!/usr/bin/env python3
"""
Symbolic Chain Compressor - Replace repeated identifiers with symbols
Weekend Hacker Edition - Keep it under 100 lines
"""

import json
import sys
import re
from typing import Dict, List, Any, Tuple
from collections import Counter

class SymbolicChainCompressor:
    """Compresses JSON by replacing repeated strings with symbols"""
    
    def __init__(self):
        self.symbol_map = {}
        self.reverse_map = {}
        self.symbol_counter = 1
    
    def compress(self, data: Any) -> Tuple[Any, Dict[str, str]]:
        """Compress data by replacing repeated strings with symbols"""
        # First pass: collect string frequencies
        string_counts = self._collect_strings(data)
        
        # Create symbol mappings for frequent strings (threshold: appears 2+ times)
        frequent_strings = {s: count for s, count in string_counts.items() 
                          if count >= 2 and len(s) > 3}  # Only compress strings > 3 chars
        
        for string in sorted(frequent_strings.keys(), key=len, reverse=True):
            symbol = f"§{self.symbol_counter}"
            self.symbol_map[string] = symbol
            self.reverse_map[symbol] = string
            self.symbol_counter += 1
        
        # Second pass: replace strings with symbols
        compressed_data = self._replace_strings(data)
        
        return compressed_data, self.reverse_map
    
    def _collect_strings(self, data: Any) -> Counter:
        """Recursively collect all strings and their frequencies"""
        strings = Counter()
        
        if isinstance(data, str):
            strings[data] += 1
        elif isinstance(data, dict):
            for key, value in data.items():
                strings[key] += 1
                strings.update(self._collect_strings(value))
        elif isinstance(data, list):
            for item in data:
                strings.update(self._collect_strings(item))
        
        return strings
    
    def _replace_strings(self, data: Any) -> Any:
        """Recursively replace strings with symbols"""
        if isinstance(data, str):
            return self.symbol_map.get(data, data)
        elif isinstance(data, dict):
            return {self.symbol_map.get(k, k): self._replace_strings(v) 
                   for k, v in data.items()}
        elif isinstance(data, list):
            return [self._replace_strings(item) for item in data]
        else:
            return data
    
    def decompress(self, compressed_data: Any, symbol_map: Dict[str, str]) -> Any:
        """Decompress data by replacing symbols with original strings"""
        if isinstance(compressed_data, str):
            return symbol_map.get(compressed_data, compressed_data)
        elif isinstance(compressed_data, dict):
            return {symbol_map.get(k, k): self.decompress(v, symbol_map) 
                   for k, v in compressed_data.items()}
        elif isinstance(compressed_data, list):
            return [self.decompress(item, symbol_map) for item in compressed_data]
        else:
            return compressed_data

def calculate_compression_ratio(original: str, compressed: str) -> float:
    """Calculate compression ratio as percentage reduction"""
    original_size = len(original)
    compressed_size = len(compressed)
    return (original_size - compressed_size) / original_size

def main():
    """CLI entry point"""
    if len(sys.argv) != 2:
        print("Usage: python symbolic_chain.py <holoforms_file>")
        sys.exit(1)
    
    holoforms_file = sys.argv[1]
    
    try:
        # Load holoforms
        with open(holoforms_file, 'r') as f:
            holoforms = json.load(f)
        
        # Compress
        compressor = SymbolicChainCompressor()
        compressed_data, symbol_map = compressor.compress(holoforms)
        
        # Calculate sizes
        original_json = json.dumps(holoforms, separators=(',', ':'))
        compressed_json = json.dumps(compressed_data, separators=(',', ':'))
        symbol_map_json = json.dumps(symbol_map, separators=(',', ':'))
        
        # Total compressed size includes the symbol dictionary
        total_compressed_size = len(compressed_json) + len(symbol_map_json)
        compression_ratio = calculate_compression_ratio(original_json, compressed_json + symbol_map_json)
        
        print("🧬 Symbolic Chain Compression")
        print("=" * 50)
        print(f"Original size: {len(original_json)} characters")
        print(f"Compressed data: {len(compressed_json)} characters")
        print(f"Symbol dictionary: {len(symbol_map_json)} characters")
        print(f"Total compressed: {total_compressed_size} characters")
        print(f"Compression ratio: {compression_ratio:.1%}")
        print(f"Symbols created: {len(symbol_map)}")
        
        if compression_ratio > 0:
            print(f"\n✅ {compression_ratio:.0%} smaller!")
        else:
            print(f"\n❌ No compression achieved (data too small/unique)")
        
        # Save compressed version
        output = {
            "compressed_data": compressed_data,
            "symbol_map": symbol_map,
            "metadata": {
                "original_size": len(original_json),
                "compressed_size": total_compressed_size,
                "compression_ratio": compression_ratio,
                "symbols_used": len(symbol_map)
            }
        }
        
        with open('compressed_holoforms.json', 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"\n💾 Compressed version saved to compressed_holoforms.json")
        
        # Show symbol mappings
        if symbol_map:
            print(f"\nSymbol Mappings:")
            for symbol, original in list(symbol_map.items())[:5]:  # Show first 5
                print(f"  {symbol} → {original[:30]}{'...' if len(original) > 30 else ''}")
            if len(symbol_map) > 5:
                print(f"  ... and {len(symbol_map) - 5} more")
        
    except FileNotFoundError:
        print(f"Error: File '{holoforms_file}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()