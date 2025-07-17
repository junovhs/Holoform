import sys
import os
import tiktoken
import json
from differential_analyzer import DifferentialAnalyzer

# Add the parent directory to the path so we can import the module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def count_tokens(text, model="gpt-4"):
    """Count the number of tokens in a text string."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")  # Default to cl100k_base
    
    return len(encoding.encode(text))

def calculate_compression_ratio(original, compressed):
    """Calculate the compression ratio between original and compressed text."""
    original_tokens = count_tokens(original)
    compressed_tokens = count_tokens(compressed)
    
    if original_tokens == 0:
        return 0, 0, 0
    
    compression_ratio = (original_tokens - compressed_tokens) / original_tokens * 100
    return compression_ratio, original_tokens, compressed_tokens

def manual_holochain_conversion(code_pattern, pattern_type, scale=1):
    """
    Manually convert code patterns to HoloChain notation for testing at different scales.
    This is used for the scale tests where we want to simulate larger codebases.
    """
    if pattern_type == "state_modification":
        if scale == 1:
            return "G:!email->status=invalid->login=0"
        elif scale == 10:
            chains = []
            for i in range(10):
                chains.append(f"G:condition_{i}->obj.attr_{i}=value_{i}")
            return "\n".join(chains)
        elif scale == 100:
            chains = []
            for i in range(100):
                chains.append(f"G:condition_{i}->obj.attr_{i}=value_{i}")
            return "\n".join(chains)
    
    elif pattern_type == "selection":
        if scale == 1:
            return "S:x < 3 <= results::x * 2"
        elif scale == 10:
            chains = []
            for i in range(10):
                chains.append(f"S:condition_{i} <= results_{i}::transform_{i}")
            return "\n".join(chains)
        elif scale == 100:
            chains = []
            for i in range(100):
                chains.append(f"S:condition_{i} <= results_{i}::transform_{i}")
            return "\n".join(chains)
    
    elif pattern_type == "resource":
        if scale == 1:
            return "R:open('file.txt') -> f\nG:block_exit(f) -> f.close()"
        elif scale == 10:
            chains = []
            for i in range(10):
                chains.append(f"R:open('file_{i}.txt') -> f_{i}")
                chains.append(f"G:block_exit(f_{i}) -> f_{i}.close()")
            return "\n".join(chains)
        elif scale == 100:
            chains = []
            for i in range(100):
                chains.append(f"R:open('file_{i}.txt') -> f_{i}")
                chains.append(f"G:block_exit(f_{i}) -> f_{i}.close()")
            return "\n".join(chains)
    
    return "UNANALYZED_PATTERN"

def generate_code_at_scale(pattern_type, scale=1):
    """Generate code patterns at different scales."""
    if pattern_type == "state_modification":
        if scale == 1:
            return """
if not user.email:
    user.status = "invalid"
    user.login_count = 0
"""
        elif scale == 10:
            code = ""
            for i in range(10):
                code += f"""
if condition_{i}:
    obj.attr_{i} = value_{i}
"""
            return code
        elif scale == 100:
            code = ""
            for i in range(100):
                code += f"""
if condition_{i}:
    obj.attr_{i} = value_{i}
"""
            return code
    
    elif pattern_type == "selection":
        if scale == 1:
            return """
results = []
for x in items:
    if x < 3:
        results.append(x * 2)
"""
        elif scale == 10:
            code = ""
            for i in range(10):
                code += f"""
results_{i} = []
for x in items_{i}:
    if condition_{i}:
        results_{i}.append(transform_{i})
"""
            return code
        elif scale == 100:
            code = ""
            for i in range(100):
                code += f"""
results_{i} = []
for x in items_{i}:
    if condition_{i}:
        results_{i}.append(transform_{i})
"""
            return code
    
    elif pattern_type == "resource":
        if scale == 1:
            return """
with open('file.txt', 'r') as f:
    content = f.read()
    process(content)
"""
        elif scale == 10:
            code = ""
            for i in range(10):
                code += f"""
with open('file_{i}.txt', 'r') as f_{i}:
    content_{i} = f_{i}.read()
    process(content_{i})
"""
            return code
        elif scale == 100:
            code = ""
            for i in range(100):
                code += f"""
with open('file_{i}.txt', 'r') as f_{i}:
    content_{i} = f_{i}.read()
    process(content_{i})
"""
            return code
    
    return ""

def run_token_efficiency_experiment():
    """Run the token efficiency experiment."""
    print("=== Token Efficiency Experiment ===")
    print("Measuring how token compression scales with codebase size\n")
    
    # Define the patterns and scales to test
    patterns = ["state_modification", "selection", "resource"]
    scales = [1, 10, 100]
    
    results = {}
    
    for pattern in patterns:
        pattern_results = {}
        
        for scale in scales:
            # Generate code at this scale
            code = generate_code_at_scale(pattern, scale)
            
            # Convert to HoloChain (manually for consistent comparison)
            holochain = manual_holochain_conversion(code, pattern, scale)
            
            # Calculate compression metrics
            compression_ratio, original_tokens, compressed_tokens = calculate_compression_ratio(code, holochain)
            
            # Store results
            pattern_results[str(scale)] = {
                "original_tokens": original_tokens,
                "compressed_tokens": compressed_tokens,
                "compression_ratio": compression_ratio
            }
            
            # Print results
            print(f"Pattern: {pattern}, Scale: {scale}")
            print(f"Original Tokens: {original_tokens}")
            print(f"Compressed Tokens: {compressed_tokens}")
            print(f"Compression Ratio: {compression_ratio:.2f}%")
            print("-" * 60)
        
        results[pattern] = pattern_results
    
    # Calculate overall compression at each scale
    print("\n=== Overall Results ===")
    
    for scale in scales:
        total_original = sum(results[pattern][str(scale)]["original_tokens"] for pattern in patterns)
        total_compressed = sum(results[pattern][str(scale)]["compressed_tokens"] for pattern in patterns)
        overall_ratio = (total_original - total_compressed) / total_original * 100 if total_original > 0 else 0
        
        print(f"Scale {scale}:")
        print(f"  Total Original Tokens: {total_original}")
        print(f"  Total Compressed Tokens: {total_compressed}")
        print(f"  Overall Compression Ratio: {overall_ratio:.2f}%")
    
    # Save results to JSON
    with open("token_efficiency_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\nResults saved to token_efficiency_results.json")
    
    # Analyze the trend
    print("\n=== Compression Trend Analysis ===")
    for pattern in patterns:
        ratios = [results[pattern][str(scale)]["compression_ratio"] for scale in scales]
        print(f"Pattern: {pattern}")
        print(f"  Compression Ratios: {', '.join(f'{r:.2f}%' for r in ratios)}")
        
        if ratios[0] < ratios[-1]:
            print("  Trend: Compression ratio INCREASES with scale")
        elif ratios[0] > ratios[-1]:
            print("  Trend: Compression ratio DECREASES with scale")
        else:
            print("  Trend: Compression ratio STABLE with scale")
    
    print("\n=== Experiment Complete ===")

if __name__ == "__main__":
    run_token_efficiency_experiment()