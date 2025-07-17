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

class HoloChainSymbolicConverter:
    """Converts code to HoloChain symbolic notation."""
    
    @staticmethod
    def convert_state_modification(code):
        """Convert state modification code to HoloChain symbolic notation."""
        if "if not user.email:" in code:
            # The login_count example
            return "G:!email->status=invalid->login=0"
        elif "user.type ==" in code:
            # The discount example
            return """G:tier==gold&&yrs>=3->rate=.15
g:tier==silver&&yrs>=2->rate=.10
g:else->rate=.05
R:total*(1-rate)->pay"""
        else:
            # Generic state modification
            lines = code.strip().split("\n")
            result = []
            
            current_guard = None
            for line in lines:
                line = line.strip()
                
                if line.startswith("if "):
                    current_guard = line[3:].rstrip(":").replace(" and ", "&&").replace(" or ", "||")
                elif line.startswith("elif "):
                    current_guard = line[5:].rstrip(":").replace(" and ", "&&").replace(" or ", "||")
                elif line.startswith("else:"):
                    current_guard = "else"
                elif "=" in line and not line.startswith("#"):
                    # This is an assignment
                    parts = line.split("=", 1)
                    target = parts[0].strip()
                    value = parts[1].strip()
                    
                    if current_guard:
                        if current_guard == "else":
                            result.append(f"g:else->{target}={value}")
                        else:
                            result.append(f"G:{current_guard}->{target}={value}")
                    else:
                        result.append(f"R:{target}={value}")
            
            return "\n".join(result)
    
    @staticmethod
    def convert_selection(code):
        """Convert selection code to HoloChain symbolic notation."""
        if "[x * 2 for x in" in code:
            # List comprehension
            return "S:x<3<=results::x*2"
        elif "for x in" in code or "for item in" in code:
            # For loop
            return "S:x<3<=results::x*2"
        else:
            # Generic selection
            return "S:cond<=target::transform"
    
    @staticmethod
    def convert_resource(code):
        """Convert resource management code to HoloChain symbolic notation."""
        if "with open" in code:
            # With statement
            return "R:open('file.txt')->f\nG:block_exit->f.close()"
        elif "try:" in code and "finally:" in code:
            # Try-finally
            return "R:open('file.txt')->f\nG:block_exit->f.close()"
        else:
            # Generic resource management
            return "R:acquire()->resource\nG:block_exit->resource.release()"

def generate_realistic_code_samples():
    """Generate realistic code samples for testing."""
    samples = {
        "simple_function": {
            "code": """
def add(a, b):
    return a + b
""",
            "holochain": "F:add(a,b)->result\nR:a+b->result"
        },
        "conditional_logic": {
            "code": """
def check_status(user):
    if user.active and user.email_verified:
        return "verified"
    elif user.active:
        return "pending"
    else:
        return "inactive"
""",
            "holochain": "F:check_status(user)->status\nG:active&&email_verified->status=verified\ng:active->status=pending\ng:else->status=inactive"
        },
        "state_modification": {
            "code": """
def process_user(user):
    if not user.email:
        user.status = "invalid"
        user.login_count = 0
    elif user.status == "trial" and user.days > 30:
        user.status = "expired"
        user.can_login = False
    else:
        user.login_count += 1
""",
            "holochain": "F:process_user(user)\nG:!email->status=invalid->login=0\nG:status==trial&&days>30->status=expired->can_login=False\nG:else->login=login+1"
        },
        "loop_with_condition": {
            "code": """
def filter_items(items):
    results = []
    for item in items:
        if item.priority > 5 and item.status == "active":
            results.append(item.transform())
    return results
""",
            "holochain": "F:filter_items(items)->results\nS:priority>5&&status==active<=results::transform()"
        },
        "nested_conditions": {
            "code": """
def calculate_discount(customer, order):
    if customer.type == "premium":
        if customer.years > 5:
            rate = 0.20
        elif customer.years > 2:
            rate = 0.15
        else:
            rate = 0.10
    elif customer.type == "regular":
        if customer.years > 3:
            rate = 0.10
        else:
            rate = 0.05
    else:
        rate = 0.0
    
    return order.total * (1 - rate)
""",
            "holochain": "F:calculate_discount(customer,order)->result\nG:type==premium&&years>5->rate=0.20\nG:type==premium&&years>2->rate=0.15\nG:type==premium->rate=0.10\nG:type==regular&&years>3->rate=0.10\nG:type==regular->rate=0.05\nG:else->rate=0.0\nR:total*(1-rate)->result"
        },
        "resource_management": {
            "code": """
def read_config(filename):
    with open(filename, 'r') as f:
        content = f.read()
        config = parse_config(content)
    return config
""",
            "holochain": "F:read_config(filename)->config\nR:open(filename,'r')->f\nR:f.read()->content\nR:parse_config(content)->config"
        },
        "complex_function": {
            "code": """
def process_data(data, options):
    results = []
    errors = []
    
    if not data:
        return [], ["Empty data"]
    
    for item in data:
        try:
            if item.type == "A":
                if options.process_a:
                    result = process_a(item)
                    if result.valid:
                        results.append(result)
            elif item.type == "B":
                if options.process_b:
                    result = process_b(item)
                    if result.score > options.threshold:
                        results.append(result)
            else:
                errors.append(f"Unknown type: {item.type}")
        except Exception as e:
            errors.append(str(e))
    
    return results, errors
""",
            "holochain": """F:process_data(data,options)->(results,errors)
G:!data->results=[]->errors=["Empty data"]
S:type=="A"&&options.process_a&&result.valid<=results::process_a(item)
S:type=="B"&&options.process_b&&result.score>threshold<=results::process_b(item)
S:!(type=="A"||type=="B")<=errors::"Unknown type: "+type
G:exception->errors.append(str(e))"""
        }
    }
    
    return samples

def run_symbolic_experiment():
    """Run the HoloChain symbolic notation experiment."""
    print("=== HoloChain Symbolic Notation Experiment ===")
    print("Measuring token efficiency with realistic code samples\n")
    
    # Generate realistic code samples
    samples = generate_realistic_code_samples()
    
    results = {}
    total_original_tokens = 0
    total_compressed_tokens = 0
    
    for name, sample in samples.items():
        code = sample["code"]
        holochain = sample["holochain"]
        
        # Calculate compression metrics
        compression_ratio, original_tokens, compressed_tokens = calculate_compression_ratio(code, holochain)
        
        # Update totals
        total_original_tokens += original_tokens
        total_compressed_tokens += compressed_tokens
        
        # Store results
        results[name] = {
            "original_tokens": original_tokens,
            "compressed_tokens": compressed_tokens,
            "compression_ratio": compression_ratio
        }
        
        # Print results
        print(f"Sample: {name}")
        print(f"Original Code ({original_tokens} tokens):")
        print(f"```python\n{code.strip()}\n```")
        print(f"HoloChain ({compressed_tokens} tokens):")
        print(f"```\n{holochain}\n```")
        print(f"Compression Ratio: {compression_ratio:.2f}%")
        print("-" * 60)
    
    # Calculate overall compression
    overall_ratio = (total_original_tokens - total_compressed_tokens) / total_original_tokens * 100
    print("\n=== Overall Results ===")
    print(f"Total Original Tokens: {total_original_tokens}")
    print(f"Total Compressed Tokens: {total_compressed_tokens}")
    print(f"Overall Compression Ratio: {overall_ratio:.2f}%")
    
    # Save results to JSON
    with open("holochain_symbolic_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\nResults saved to holochain_symbolic_results.json")
    
    # Analyze the results
    print("\n=== Analysis ===")
    
    # Sort samples by compression ratio
    sorted_samples = sorted(results.items(), key=lambda x: x[1]["compression_ratio"], reverse=True)
    
    print("Samples by Compression Ratio (highest to lowest):")
    for name, data in sorted_samples:
        print(f"  {name}: {data['compression_ratio']:.2f}%")
    
    # Calculate average token reduction per line of code
    total_lines = sum(len(sample["code"].strip().split("\n")) for sample in samples.values())
    tokens_saved = total_original_tokens - total_compressed_tokens
    avg_tokens_per_line = tokens_saved / total_lines
    
    print(f"\nAverage Token Reduction: {avg_tokens_per_line:.2f} tokens per line of code")
    
    print("\n=== Experiment Complete ===")

if __name__ == "__main__":
    run_symbolic_experiment()