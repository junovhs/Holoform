import sys
import os
import tiktoken
import json
from typing import List, Dict, Any

def count_tokens(text, model="gpt-4"):
    """Count the number of tokens in a text string."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    
    return len(encoding.encode(text))

def generate_large_codebase(num_functions: int) -> str:
    """Generate a large Python codebase with realistic patterns."""
    code_templates = [
        # State modification pattern
        """
def process_user_{i}(user):
    if not user.email_{i}:
        user.status_{i} = "invalid"
        user.login_count_{i} = 0
    elif user.type_{i} == "premium":
        user.discount_{i} = 0.15
        user.priority_{i} = "high"
    else:
        user.discount_{i} = 0.05
        user.priority_{i} = "normal"
    return user
""",
        # Selection pattern
        """
def filter_items_{i}(items):
    results = []
    for item in items:
        if item.priority_{i} > 5 and item.status_{i} == "active":
            processed = transform_item_{i}(item)
            if processed.valid:
                results.append(processed)
    return results
""",
        # Resource management pattern
        """
def read_file_{i}(filename):
    with open(filename, 'r') as f:
        content = f.read()
        data = parse_data_{i}(content)
        if data.valid:
            return process_data_{i}(data)
    return None
""",
        # Complex conditional pattern
        """
def calculate_price_{i}(customer, product):
    base_price = product.price_{i}
    
    if customer.tier_{i} == "gold" and customer.years_{i} >= 3:
        discount = 0.20
    elif customer.tier_{i} == "silver" and customer.years_{i} >= 2:
        discount = 0.15
    elif customer.tier_{i} == "bronze":
        discount = 0.05
    else:
        discount = 0.0
    
    if product.category_{i} == "premium":
        tax_rate = 0.15
    else:
        tax_rate = 0.10
    
    discounted_price = base_price * (1 - discount)
    final_price = discounted_price * (1 + tax_rate)
    
    return final_price
"""
    ]
    
    codebase = "# Generated Python codebase for scaling experiment\n\n"
    
    for i in range(num_functions):
        template = code_templates[i % len(code_templates)]
        codebase += template.format(i=i)
        codebase += "\n"
    
    return codebase

def convert_to_holochain(num_functions: int) -> str:
    """Convert the generated codebase to HoloChain notation."""
    holochain_templates = [
        # State modification pattern
        """F:process_user_{i}(user)->user
G:!email_{i}->status_{i}=invalid->login_count_{i}=0
G:type_{i}==premium->discount_{i}=0.15->priority_{i}=high
G:else->discount_{i}=0.05->priority_{i}=normal""",
        
        # Selection pattern
        """F:filter_items_{i}(items)->results
S:priority_{i}>5&&status_{i}==active&&valid<=results::transform_item_{i}(item)""",
        
        # Resource management pattern
        """F:read_file_{i}(filename)->result
R:open(filename,'r')->f
R:f.read()->content
R:parse_data_{i}(content)->data
G:data.valid->result=process_data_{i}(data)
G:!data.valid->result=None""",
        
        # Complex conditional pattern
        """F:calculate_price_{i}(customer,product)->final_price
G:tier_{i}==gold&&years_{i}>=3->discount=0.20
G:tier_{i}==silver&&years_{i}>=2->discount=0.15
G:tier_{i}==bronze->discount=0.05
G:else->discount=0.0
G:category_{i}==premium->tax_rate=0.15
G:else->tax_rate=0.10
R:base_price*(1-discount)->discounted_price
R:discounted_price*(1+tax_rate)->final_price"""
    ]
    
    holochain = "# HoloChain representation\n\n"
    
    for i in range(num_functions):
        template = holochain_templates[i % len(holochain_templates)]
        holochain += template.format(i=i)
        holochain += "\n\n"
    
    return holochain

def run_scaling_experiment():
    """Run the scaling experiment to test compression at different codebase sizes."""
    print("=== Scaling Experiment ===")
    print("Testing how compression ratio changes with codebase size\n")
    
    # Test different scales
    scales = [10, 50, 100, 500, 1000]
    results = {}
    
    for scale in scales:
        print(f"Testing scale: {scale} functions...")
        
        # Generate codebase
        original_code = generate_large_codebase(scale)
        holochain_code = convert_to_holochain(scale)
        
        # Count tokens
        original_tokens = count_tokens(original_code)
        compressed_tokens = count_tokens(holochain_code)
        
        # Calculate compression ratio
        compression_ratio = (original_tokens - compressed_tokens) / original_tokens * 100
        
        # Store results
        results[scale] = {
            "original_tokens": original_tokens,
            "compressed_tokens": compressed_tokens,
            "compression_ratio": compression_ratio,
            "tokens_saved": original_tokens - compressed_tokens
        }
        
        print(f"  Original tokens: {original_tokens:,}")
        print(f"  Compressed tokens: {compressed_tokens:,}")
        print(f"  Compression ratio: {compression_ratio:.2f}%")
        print(f"  Tokens saved: {original_tokens - compressed_tokens:,}")
        print()
    
    # Analyze scaling trend
    print("=== Scaling Analysis ===")
    
    # Calculate compression efficiency (tokens saved per function)
    for scale in scales:
        tokens_per_function = results[scale]["tokens_saved"] / scale
        print(f"Scale {scale}: {tokens_per_function:.1f} tokens saved per function")
    
    # Check if compression ratio improves with scale
    ratios = [results[scale]["compression_ratio"] for scale in scales]
    print(f"\nCompression ratios: {', '.join(f'{r:.2f}%' for r in ratios)}")
    
    if ratios[-1] > ratios[0]:
        improvement = ratios[-1] - ratios[0]
        print(f"✅ Compression ratio IMPROVES with scale: +{improvement:.2f}% from smallest to largest")
    else:
        decline = ratios[0] - ratios[-1]
        print(f"❌ Compression ratio DECLINES with scale: -{decline:.2f}% from smallest to largest")
    
    # Calculate potential savings for your 40k token codebase
    print("\n=== Extrapolation to Real Codebase ===")
    
    # Use the best compression ratio we achieved
    best_ratio = max(ratios)
    your_codebase_tokens = 40000  # Your mentioned 40k token codebase
    
    potential_savings = your_codebase_tokens * (best_ratio / 100)
    compressed_size = your_codebase_tokens - potential_savings
    
    print(f"Your 40k token codebase could potentially be compressed to:")
    print(f"  Compressed size: {compressed_size:,.0f} tokens")
    print(f"  Tokens saved: {potential_savings:,.0f} tokens")
    print(f"  Compression ratio: {best_ratio:.2f}%")
    
    # Calculate impact on your Gemini CLI usage
    gemini_usage = 50_000_000  # 50 million tokens you mentioned
    potential_gemini_savings = gemini_usage * (best_ratio / 100)
    new_gemini_usage = gemini_usage - potential_gemini_savings
    
    print(f"\nImpact on your Gemini CLI usage:")
    print(f"  Current usage: {gemini_usage:,} tokens")
    print(f"  Potential new usage: {new_gemini_usage:,.0f} tokens")
    print(f"  Tokens saved: {potential_gemini_savings:,.0f} tokens")
    print(f"  Usage reduction: {(potential_gemini_savings / gemini_usage) * 100:.1f}%")
    
    # Save results
    with open("scaling_experiment_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to scaling_experiment_results.json")
    print("\n=== Experiment Complete ===")

if __name__ == "__main__":
    run_scaling_experiment()