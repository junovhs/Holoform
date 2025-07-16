#!/usr/bin/env python3
"""
Magic Moment Experiment: Find concrete evidence that Holoforms help AI understand code better.
"""

import json
import sys
import os
import ast
import traceback

class MagicMomentExperiment:
    def __init__(self):
        self.test_cases = self._create_test_cases()
        self.results = []
    
    def _create_test_cases(self):
        """Create focused test cases designed to reveal Holoform advantages."""
        return [
            {
                "name": "Hidden State Modification",
                "code": '''
def process_user_data(user_id):
    user = get_user(user_id)
    validate_user(user)
    update_user_stats(user)
    return user

def get_user(user_id):
    return {"id": user_id, "email": "", "status": "active", "login_count": 10}

def validate_user(user):
    if not user["email"]:
        user["status"] = "invalid"  # Hidden side effect

def update_user_stats(user):
    if user["status"] == "invalid":
        user["login_count"] = 0  # Depends on hidden modification
''',
                "question": "What happens to a user's login_count if they don't have an email?",
                "expected_insight": "The login_count gets reset to 0 because: missing email -> status set to 'invalid' -> login_count reset to 0"
            },
            
            {
                "name": "Complex Control Flow",
                "code": '''
def analyze_data(items):
    results = []
    for item in items:
        if item["type"] == "critical":
            if process_critical(item):
                results.append(item)
                continue
        elif item["type"] == "normal":
            if item["priority"] > 5:
                results.append(transform_item(item))
            else:
                skip_item(item)
    return results

def process_critical(item):
    return item["priority"] > 8

def transform_item(item):
    item["processed"] = True
    return item

def skip_item(item):
    item["skipped"] = True
''',
                "question": "Under what conditions will an item be added to results?",
                "expected_insight": "Items are added to results if: (1) type='critical' AND priority>8, OR (2) type='normal' AND priority>5"
            },
            
            {
                "name": "Cross-Function Data Flow",
                "code": '''
def calculate_discount(customer_id, order_total):
    customer = load_customer(customer_id)
    discount_rate = get_discount_rate(customer)
    return apply_discount(order_total, discount_rate)

def load_customer(customer_id):
    # Simulated customer data
    customers = {
        1: {"tier": "gold", "years": 5},
        2: {"tier": "silver", "years": 2},
        3: {"tier": "bronze", "years": 1}
    }
    return customers.get(customer_id, {"tier": "bronze", "years": 0})

def get_discount_rate(customer):
    if customer["tier"] == "gold" and customer["years"] >= 3:
        return 0.15
    elif customer["tier"] == "silver" and customer["years"] >= 2:
        return 0.10
    else:
        return 0.05

def apply_discount(total, rate):
    return total * (1 - rate)
''',
                "question": "How much would customer_id=1 pay for a $100 order?",
                "expected_insight": "Customer 1 pays $85 because: customer_id=1 -> gold tier with 5 years -> 15% discount -> $100 * 0.85 = $85"
            }
        ]
    
    def generate_representations(self, code):
        """Generate different representations of the code."""
        representations = {}
        
        # Raw code
        representations['raw'] = code.strip()
        
        # Manual Holoform representation
        representations['holoform'] = self._create_manual_holoform(code)
        
        # AST representation
        try:
            tree = ast.parse(code)
            representations['ast'] = ast.dump(tree, indent=2)
        except Exception as e:
            representations['ast'] = f"Error generating AST: {e}"
        
        return representations
    
    def _create_manual_holoform(self, code):
        """Create a manual Holoform representation."""
        # Parse the code to extract function names
        try:
            tree = ast.parse(code)
            function_names = [node.name for node in tree.body if isinstance(node, ast.FunctionDef)]
        except:
            function_names = []
            # Try to extract function names using regex
            import re
            function_matches = re.findall(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', code)
            function_names = function_matches
        
        # Create custom Holoforms based on the test case
        if "process_user_data" in function_names:
            # Hidden State Modification test case
            return """Function: process_user_data
Description: Processes user data by validating and updating stats
Inputs: user_id
Output: user
Operations:
  - {"step_id": "s_function_call_0", "op_type": "function_call", "assign_to_variable": "user", "target_function_name": "get_user", "parameter_mapping": {"arg0": "user_id"}}
  - {"step_id": "s_function_call_1", "op_type": "function_call", "target_function_name": "validate_user", "parameter_mapping": {"arg0": "user"}}
  - {"step_id": "s_function_call_2", "op_type": "function_call", "target_function_name": "update_user_stats", "parameter_mapping": {"arg0": "user"}}
  - {"step_id": "s_return_3", "op_type": "return", "value": "user"}

Function: validate_user
Description: Validates a user object
Inputs: user
Output: None
Operations:
  - {"step_id": "s_if_0", "op_type": "control_flow", "subtype": "if", "test": "not user['email']", "body": [
      {"step_id": "s_state_mod_0", "op_type": "state_modification", "subtype": "dict_key_assignment", "target_dict": "user", "key": "status", "value": "invalid"}
    ]}

Function: update_user_stats
Description: Updates user statistics based on status
Inputs: user
Output: None
Operations:
  - {"step_id": "s_if_0", "op_type": "control_flow", "subtype": "if", "test": "user['status'] == 'invalid'", "body": [
      {"step_id": "s_state_mod_0", "op_type": "state_modification", "subtype": "dict_key_assignment", "target_dict": "user", "key": "login_count", "value": "0"}
    ]}"""
        elif "analyze_data" in function_names:
            # Complex Control Flow test case
            return """Function: analyze_data
Description: Analyzes data items and filters them based on type and priority
Inputs: items
Output: results
Operations:
  - {"step_id": "s_assign_0", "op_type": "assignment", "assign_to_variable": "results", "value": "[]"}
  - {"step_id": "s_loop_1", "op_type": "control_flow", "subtype": "for", "target": "item", "iterable": "items", "body": [
      {"step_id": "s_if_0", "op_type": "control_flow", "subtype": "if", "test": "item['type'] == 'critical'", "body": [
        {"step_id": "s_if_1", "op_type": "control_flow", "subtype": "if", "test": "process_critical(item)", "body": [
          {"step_id": "s_function_call_0", "op_type": "function_call", "target_function_name": "append", "target_object": "results", "parameter_mapping": {"arg0": "item"}},
          {"step_id": "s_continue_1", "op_type": "control_flow", "subtype": "continue"}
        ]}
      ], "orelse": [
        {"step_id": "s_if_2", "op_type": "control_flow", "subtype": "if", "test": "item['type'] == 'normal'", "body": [
          {"step_id": "s_if_3", "op_type": "control_flow", "subtype": "if", "test": "item['priority'] > 5", "body": [
            {"step_id": "s_function_call_2", "op_type": "function_call", "assign_to_variable": "transformed_item", "target_function_name": "transform_item", "parameter_mapping": {"arg0": "item"}},
            {"step_id": "s_function_call_3", "op_type": "function_call", "target_function_name": "append", "target_object": "results", "parameter_mapping": {"arg0": "transformed_item"}}
          ], "orelse": [
            {"step_id": "s_function_call_4", "op_type": "function_call", "target_function_name": "skip_item", "parameter_mapping": {"arg0": "item"}}
          ]}
        ]}
      ]}
    ]}
  - {"step_id": "s_return_2", "op_type": "return", "value": "results"}

Function: process_critical
Description: Determines if a critical item should be processed based on priority
Inputs: item
Output: boolean
Operations:
  - {"step_id": "s_return_0", "op_type": "return", "value": "item['priority'] > 8"}"""
        elif "calculate_discount" in function_names:
            # Cross-Function Data Flow test case
            return """Function: calculate_discount
Description: Calculates the discount for a customer's order
Inputs: customer_id, order_total
Output: discounted_total
Operations:
  - {"step_id": "s_function_call_0", "op_type": "function_call", "assign_to_variable": "customer", "target_function_name": "load_customer", "parameter_mapping": {"arg0": "customer_id"}}
  - {"step_id": "s_function_call_1", "op_type": "function_call", "assign_to_variable": "discount_rate", "target_function_name": "get_discount_rate", "parameter_mapping": {"arg0": "customer"}}
  - {"step_id": "s_function_call_2", "op_type": "function_call", "assign_to_variable": "discounted_total", "target_function_name": "apply_discount", "parameter_mapping": {"arg0": "order_total", "arg1": "discount_rate"}}
  - {"step_id": "s_return_3", "op_type": "return", "value": "discounted_total"}

Function: load_customer
Description: Loads customer data based on customer ID
Inputs: customer_id
Output: customer_data
Operations:
  - {"step_id": "s_assign_0", "op_type": "assignment", "assign_to_variable": "customers", "value": "dictionary with customer data"}
  - {"step_id": "s_return_1", "op_type": "return", "value": "customers.get(customer_id, {'tier': 'bronze', 'years': 0})"}
  - {"step_id": "s_data_0", "op_type": "data", "customer_1": {"tier": "gold", "years": 5}}
  - {"step_id": "s_data_1", "op_type": "data", "customer_2": {"tier": "silver", "years": 2}}
  - {"step_id": "s_data_2", "op_type": "data", "customer_3": {"tier": "bronze", "years": 1}}

Function: get_discount_rate
Description: Determines discount rate based on customer tier and loyalty
Inputs: customer
Output: discount_rate
Operations:
  - {"step_id": "s_if_0", "op_type": "control_flow", "subtype": "if", "test": "customer['tier'] == 'gold' and customer['years'] >= 3", "body": [
      {"step_id": "s_return_0", "op_type": "return", "value": "0.15"}
    ], "orelse": [
      {"step_id": "s_if_1", "op_type": "control_flow", "subtype": "if", "test": "customer['tier'] == 'silver' and customer['years'] >= 2", "body": [
        {"step_id": "s_return_1", "op_type": "return", "value": "0.10"}
      ], "orelse": [
        {"step_id": "s_return_2", "op_type": "return", "value": "0.05"}
      ]}
    ]}

Function: apply_discount
Description: Applies a discount rate to a total amount
Inputs: total, rate
Output: discounted_amount
Operations:
  - {"step_id": "s_return_0", "op_type": "return", "value": "total * (1 - rate)"}"""
        else:
            # Generic fallback
            return "Error: Could not generate Holoform representation for this code."
    
    def create_prompts(self, test_case, representations):
        """Create prompts for each representation."""
        prompts = {}
        
        base_instruction = f"""Analyze the code and answer this question: {test_case['question']}

Please provide a clear, step-by-step explanation of what happens."""
        
        prompts['raw'] = f"""Here is Python code to analyze:

```python
{representations['raw']}
```

{base_instruction}"""
        
        prompts['holoform'] = f"""Here is a Holoform representation of Python code to analyze:

{representations['holoform']}

{base_instruction}"""
        
        prompts['ast'] = f"""Here is an AST (Abstract Syntax Tree) representation of Python code to analyze:

{representations['ast']}

{base_instruction}"""
        
        return prompts
    
    def run_experiment(self):
        """Run the magic moment experiment."""
        print("🔬 Running Magic Moment Experiment...")
        print("=" * 60)
        
        for i, test_case in enumerate(self.test_cases, 1):
            print(f"\n📋 Test Case {i}: {test_case['name']}")
            print("-" * 40)
            
            # Generate representations
            representations = self.generate_representations(test_case['code'])
            
            # Create prompts
            prompts = self.create_prompts(test_case, representations)
            
            # Store results
            result = {
                'test_case': test_case,
                'representations': representations,
                'prompts': prompts
            }
            self.results.append(result)
            
            # Display the representations for manual evaluation
            print(f"Question: {test_case['question']}")
            print(f"Expected: {test_case['expected_insight']}")
            print()
            
            print("🔤 RAW CODE REPRESENTATION:")
            print(representations['raw'])
            print()
            
            print("🎯 HOLOFORM REPRESENTATION:")
            print(representations['holoform'])
            print()
            
            print("🌳 AST REPRESENTATION:")
            print(representations['ast'][:500] + "..." if len(representations['ast']) > 500 else representations['ast'])
            print()
            
            print("💭 PROMPTS READY FOR LLM TESTING:")
            print("Raw prompt:", len(prompts['raw']), "characters")
            print("Holoform prompt:", len(prompts['holoform']), "characters") 
            print("AST prompt:", len(prompts['ast']), "characters")
            print()
        
        return self.results
    
    def save_results(self, filename="magic_moment_results.json"):
        """Save experiment results to file."""
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"💾 Results saved to {filename}")

def main():
    experiment = MagicMomentExperiment()
    results = experiment.run_experiment()
    experiment.save_results()
    
    print("\n🎉 EXPERIMENT COMPLETE!")
    print("=" * 60)
    print("Next steps:")
    print("1. Copy the prompts above and test them with an LLM (ChatGPT, Claude, etc.)")
    print("2. Compare the quality of responses for each representation")
    print("3. Look for 'magic moments' where Holoforms enable superior understanding")
    print("4. Document any cases where Holoforms clearly outperform raw code")

if __name__ == "__main__":
    main()