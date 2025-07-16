#!/usr/bin/env python3
"""
Analyze Magic Moment Experiment Results
"""

import json
import sys
import os

def load_results(filename="magic_moment_results.json"):
    """Load experiment results from file."""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading results: {e}")
        return None

def analyze_responses(results, llm_responses):
    """Analyze LLM responses for each test case and representation."""
    analysis = []
    
    for i, (result, responses) in enumerate(zip(results, llm_responses)):
        test_case = result['test_case']
        
        test_analysis = {
            'test_case': test_case['name'],
            'question': test_case['question'],
            'expected_insight': test_case['expected_insight'],
            'responses': {}
        }
        
        for rep_type, response in responses.items():
            # Score the response (0-10)
            accuracy = score_accuracy(response, test_case['expected_insight'])
            completeness = score_completeness(response, test_case['expected_insight'])
            insight_depth = score_insight_depth(response)
            
            test_analysis['responses'][rep_type] = {
                'response': response,
                'scores': {
                    'accuracy': accuracy,
                    'completeness': completeness,
                    'insight_depth': insight_depth,
                    'total': (accuracy + completeness + insight_depth) / 3
                }
            }
        
        # Determine if this is a "magic moment"
        holoform_score = test_analysis['responses']['holoform']['scores']['total']
        raw_score = test_analysis['responses']['raw']['scores']['total']
        ast_score = test_analysis['responses']['ast']['scores']['total']
        
        is_magic = holoform_score > raw_score + 1.5 and holoform_score > ast_score + 1.5
        
        test_analysis['is_magic_moment'] = is_magic
        test_analysis['score_difference'] = {
            'holoform_vs_raw': holoform_score - raw_score,
            'holoform_vs_ast': holoform_score - ast_score
        }
        
        analysis.append(test_analysis)
    
    return analysis

def score_accuracy(response, expected_insight):
    """Score how accurately the response matches the expected insight (0-10)."""
    # This is a placeholder - in a real scenario, you would implement a more sophisticated scoring algorithm
    # or have human evaluators score the responses
    return 0  # Replace with actual score

def score_completeness(response, expected_insight):
    """Score how completely the response addresses all aspects of the expected insight (0-10)."""
    # This is a placeholder
    return 0  # Replace with actual score

def score_insight_depth(response):
    """Score the depth of understanding demonstrated in the response (0-10)."""
    # This is a placeholder
    return 0  # Replace with actual score

def print_analysis(analysis):
    """Print analysis results in a readable format."""
    print("\n🔍 MAGIC MOMENT ANALYSIS")
    print("=" * 60)
    
    magic_moments = [a for a in analysis if a['is_magic_moment']]
    
    print(f"\nFound {len(magic_moments)} magic moments out of {len(analysis)} test cases.")
    
    for i, test in enumerate(analysis, 1):
        print(f"\n📋 Test Case {i}: {test['test_case']}")
        print("-" * 40)
        print(f"Question: {test['question']}")
        print(f"Expected: {test['expected_insight']}")
        print()
        
        for rep_type, resp_data in test['responses'].items():
            scores = resp_data['scores']
            print(f"{rep_type.upper()} SCORE: {scores['total']:.1f}/10 (Accuracy: {scores['accuracy']:.1f}, Completeness: {scores['completeness']:.1f}, Insight: {scores['insight_depth']:.1f})")
        
        print()
        if test['is_magic_moment']:
            print("✨ MAGIC MOMENT! ✨")
            print(f"Holoform outperformed Raw Code by {test['score_difference']['holoform_vs_raw']:.1f} points")
            print(f"Holoform outperformed AST by {test['score_difference']['holoform_vs_ast']:.1f} points")
        
        print("\nKey differences in responses:")
        # Here you would highlight key differences between the responses
        # This is a placeholder for manual analysis
    
    if magic_moments:
        print("\n✨ MAGIC MOMENT SUMMARY ✨")
        print("=" * 60)
        for moment in magic_moments:
            print(f"- {moment['test_case']}: Holoform enabled better understanding of {moment['question']}")
    
    print("\n🔬 CONCLUSION")
    print("=" * 60)
    # This is a placeholder for your conclusion
    print("Based on the analysis, Holoforms show promise for...")

def main():
    # Load experiment results
    results = load_results()
    if not results:
        print("No results found. Run magic_moment_experiment.py first.")
        return
    
    # In a real scenario, you would collect LLM responses for each prompt
    # For this example, we'll use placeholder responses
    llm_responses = []
    for result in results:
        llm_responses.append({
            'raw': "This is a placeholder response for raw code.",
            'holoform': "This is a placeholder response for Holoform representation.",
            'ast': "This is a placeholder response for AST representation."
        })
    
    # Analyze responses
    analysis = analyze_responses(results, llm_responses)
    
    # Print analysis
    print_analysis(analysis)
    
    # Save analysis
    with open("magic_moment_analysis.json", 'w') as f:
        json.dump(analysis, f, indent=2)
    print(f"\n💾 Analysis saved to magic_moment_analysis.json")

if __name__ == "__main__":
    main()