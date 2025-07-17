"""
Immediate Validation Test for HoloChain

This creates specific test cases where we know the exact correct answer,
so we can immediately validate if HoloChain preserves semantic meaning.
"""

import json
import tiktoken

def count_tokens(text):
    """Count tokens using GPT-4 tokenizer."""
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))

def create_validation_prompts():
    """Create prompts for immediate AI testing with known correct answers."""
    
    test_cases = [
        {
            "name": "Login Count Reset Logic",
            "scenario": "We need to trace when a user's login_count gets reset to 0",
            "original_code": """
def process_user_login(user):
    if not user.email:
        user.status = "invalid"
        user.login_count = 0
        return "email_required"
    
    if user.status == "banned":
        user.login_count = 0
        return "account_banned"
    
    if user.failed_attempts > 5:
        user.status = "locked"
        user.login_count = 0
        return "account_locked"
    
    user.login_count += 1
    return "login_successful"
""",
            "holochain": """
F:process_user_login(user)->result
G:!email->status=invalid->login_count=0->R:email_required
G:status==banned->login_count=0->R:account_banned
G:failed_attempts>5->status=locked->login_count=0->R:account_locked
G:else->login_count=login_count+1->R:login_successful
""",
            "question": "List ALL the conditions under which login_count gets set to 0.",
            "correct_answer": [
                "When user has no email (!email)",
                "When user status is 'banned' (status==banned)", 
                "When user has more than 5 failed attempts (failed_attempts>5)"
            ],
            "validation_criteria": "Answer must include all 3 conditions and no false conditions"
        },
        
        {
            "name": "Discount Calculation Trace",
            "scenario": "Calculate the exact discount for specific customer scenarios",
            "original_code": """
def calculate_customer_discount(customer, order_total):
    base_discount = 0.0
    
    if customer.type == "premium":
        if customer.years >= 5:
            base_discount = 0.20
        elif customer.years >= 2:
            base_discount = 0.15
        else:
            base_discount = 0.10
    elif customer.type == "regular":
        if customer.years >= 3:
            base_discount = 0.08
        else:
            base_discount = 0.05
    
    if customer.loyalty_points > 1000:
        base_discount += 0.05
    
    max_discount = 0.25
    final_discount = min(base_discount, max_discount)
    
    return order_total * final_discount
""",
            "holochain": """
F:calculate_customer_discount(customer,order_total)->discount_amount
G:type==premium&&years>=5->base_discount=0.20
G:type==premium&&years>=2->base_discount=0.15
G:type==premium->base_discount=0.10
G:type==regular&&years>=3->base_discount=0.08
G:type==regular->base_discount=0.05
G:loyalty_points>1000->base_discount=base_discount+0.05
R:min(base_discount,0.25)->final_discount
R:order_total*final_discount->discount_amount
""",
            "question": "What is the exact discount amount for: premium customer, 6 years, 1200 loyalty points, $100 order?",
            "correct_answer": "$25.00",
            "step_by_step": [
                "Premium customer with 6 years: base_discount = 0.20",
                "Loyalty points > 1000: base_discount = 0.20 + 0.05 = 0.25", 
                "Final discount = min(0.25, 0.25) = 0.25",
                "Discount amount = $100 * 0.25 = $25.00"
            ],
            "validation_criteria": "Answer must be exactly $25.00 with correct reasoning"
        },
        
        {
            "name": "Error Recovery Flow",
            "scenario": "Trace the exact sequence of operations when errors occur",
            "original_code": """
def deploy_with_rollback(config, backup_path):
    try:
        validate_config(config)
        create_backup(backup_path)
        deploy_changes(config)
        run_health_check()
        return "deployment_successful"
    except ValidationError:
        return "validation_failed"
    except BackupError:
        return "backup_failed"
    except DeploymentError:
        restore_from_backup(backup_path)
        return "deployment_failed_restored"
    except HealthCheckError:
        restore_from_backup(backup_path)
        return "health_check_failed_restored"
""",
            "holochain": """
F:deploy_with_rollback(config,backup_path)->result
G:validate_config()->create_backup()->deploy_changes()->run_health_check()->R:deployment_successful
G:ValidationError->R:validation_failed
G:BackupError->R:backup_failed
G:DeploymentError->restore_from_backup()->R:deployment_failed_restored
G:HealthCheckError->restore_from_backup()->R:health_check_failed_restored
""",
            "question": "If deployment succeeds but health check fails, what operations are performed and what is returned?",
            "correct_answer": "restore_from_backup() is called, then returns 'health_check_failed_restored'",
            "step_by_step": [
                "validate_config() succeeds",
                "create_backup() succeeds", 
                "deploy_changes() succeeds",
                "run_health_check() fails (HealthCheckError)",
                "restore_from_backup() is called",
                "Returns 'health_check_failed_restored'"
            ],
            "validation_criteria": "Must mention restore_from_backup() and correct return value"
        }
    ]
    
    return test_cases

def generate_test_prompts():
    """Generate the actual prompts to test with AI."""
    
    test_cases = create_validation_prompts()
    
    print("=== HoloChain Immediate Validation Test ===")
    print("Generated prompts for AI testing with known correct answers\n")
    
    all_prompts = []
    
    for i, case in enumerate(test_cases, 1):
        print(f"=== TEST CASE {i}: {case['name']} ===")
        print(f"Scenario: {case['scenario']}")
        print()
        
        # Create prompts for both original code and HoloChain
        original_prompt = f"""
ORIGINAL CODE TEST:

Here is some code to analyze:

```python
{case['original_code'].strip()}
```

Question: {case['question']}

Please provide a precise, step-by-step answer.
"""
        
        holochain_prompt = f"""
HOLOCHAIN TEST:

Here is a HoloChain representation to analyze:

```
{case['holochain'].strip()}
```

Question: {case['question']}

Please provide a precise, step-by-step answer.
"""
        
        # Calculate token efficiency
        original_tokens = count_tokens(case['original_code'])
        holochain_tokens = count_tokens(case['holochain'])
        compression_ratio = (original_tokens - holochain_tokens) / original_tokens * 100
        
        print(f"ORIGINAL CODE PROMPT ({original_tokens} tokens):")
        print(original_prompt)
        print()
        print(f"HOLOCHAIN PROMPT ({holochain_tokens} tokens, {compression_ratio:.1f}% compression):")
        print(holochain_prompt)
        print()
        print(f"CORRECT ANSWER: {case['correct_answer']}")
        if 'step_by_step' in case:
            print("STEP-BY-STEP:")
            for step in case['step_by_step']:
                print(f"  - {step}")
        print()
        print(f"VALIDATION CRITERIA: {case['validation_criteria']}")
        print("=" * 80)
        print()
        
        # Store prompts for later use
        all_prompts.append({
            "case_name": case['name'],
            "original_prompt": original_prompt,
            "holochain_prompt": holochain_prompt,
            "correct_answer": case['correct_answer'],
            "validation_criteria": case['validation_criteria'],
            "token_analysis": {
                "original_tokens": original_tokens,
                "holochain_tokens": holochain_tokens,
                "compression_ratio": compression_ratio
            }
        })
    
    # Save prompts to file
    with open("validation_test_prompts.json", "w") as f:
        json.dump(all_prompts, f, indent=2)
    
    print("=== TESTING INSTRUCTIONS ===")
    print("1. Copy each prompt above and test with an AI (ChatGPT, Claude, etc.)")
    print("2. Compare the AI's answers to the correct answers provided")
    print("3. Verify that both original code and HoloChain produce the same correct answer")
    print("4. Note any differences in reasoning quality or accuracy")
    print("5. Record results to validate HoloChain semantic preservation")
    print()
    print("Prompts saved to: validation_test_prompts.json")
    print()
    print("=== SUCCESS CRITERIA ===")
    print("✅ HoloChain is valid if AI gives same correct answers as original code")
    print("✅ Bonus points if HoloChain enables clearer/faster reasoning")
    print("❌ HoloChain fails if AI gives wrong answers or misses key details")
    
    return all_prompts

if __name__ == "__main__":
    generate_test_prompts()