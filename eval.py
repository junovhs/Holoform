#!/usr/bin/env python3
"""
Holoform Evaluator - Compare LLM performance on raw code vs Holoforms
Weekend Hacker Edition - Keep it under 150 lines
"""

import json
import sys
import time
from typing import Dict, List, Any

# Mock LLM interface - replace with actual LLM calls
class MockLLM:
    """Mock LLM for demonstration - replace with OpenAI/local model"""
    
    def query(self, prompt: str) -> str:
        """Mock LLM response - in real version, call actual LLM"""
        # Simple pattern matching for demo
        if "fibonacci" in prompt.lower():
            if "holoform" in prompt.lower() or "structure" in prompt.lower():
                return "Returns the nth Fibonacci number using recursion"
            else:
                return "Calculates Fibonacci sequence"
        
        elif "calculator" in prompt.lower():
            if "holoform" in prompt.lower():
                return "A calculator class that tracks operation history"
            else:
                return "Some kind of math class"
        
        elif "process_numbers" in prompt.lower():
            if "holoform" in prompt.lower():
                return "Processes a list and returns count, sum, and average statistics"
            else:
                return "Does something with numbers"
        
        return "Unknown function"

class HoloformEvaluator:
    """Evaluates LLM performance on code understanding tasks"""
    
    def __init__(self):
        self.llm = MockLLM()
        self.test_cases = [
            {
                "name": "fibonacci_purpose",
                "question": "What does this function return?",
                "expected": "nth Fibonacci number"
            },
            {
                "name": "calculator_purpose", 
                "question": "What is the main purpose of this class?",
                "expected": "calculator with history tracking"
            },
            {
                "name": "process_numbers_output",
                "question": "What does this function return?",
                "expected": "statistics dictionary with count, sum, average"
            }
        ]
    
    def evaluate_raw_code(self, source_code: str) -> Dict[str, Any]:
        """Evaluate LLM performance on raw source code"""
        results = {
            "method": "raw_code",
            "token_count": len(source_code.split()),  # Rough token estimate
            "test_results": []
        }
        
        for test_case in self.test_cases:
            prompt = f"""
            Code:
            {source_code}
            
            Question: {test_case['question']}
            Answer:"""
            
            start_time = time.time()
            response = self.llm.query(prompt)
            end_time = time.time()
            
            # Simple accuracy check
            accuracy = self._calculate_accuracy(response, test_case['expected'])
            
            results["test_results"].append({
                "test": test_case['name'],
                "response": response,
                "expected": test_case['expected'],
                "accuracy": accuracy,
                "response_time": end_time - start_time
            })
        
        return results
    
    def evaluate_holoforms(self, holoforms: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Evaluate LLM performance on Holoform representations"""
        holoform_text = json.dumps(holoforms, indent=2)
        
        results = {
            "method": "holoforms",
            "token_count": len(holoform_text.split()),  # Rough token estimate
            "test_results": []
        }
        
        for test_case in self.test_cases:
            prompt = f"""
            Holoform Structure:
            {holoform_text}
            
            Question: {test_case['question']}
            Answer:"""
            
            start_time = time.time()
            response = self.llm.query(prompt)
            end_time = time.time()
            
            accuracy = self._calculate_accuracy(response, test_case['expected'])
            
            results["test_results"].append({
                "test": test_case['name'],
                "response": response,
                "expected": test_case['expected'],
                "accuracy": accuracy,
                "response_time": end_time - start_time
            })
        
        return results
    
    def _calculate_accuracy(self, response: str, expected: str) -> float:
        """Simple accuracy calculation based on keyword matching"""
        response_lower = response.lower()
        expected_words = expected.lower().split()
        
        matches = sum(1 for word in expected_words if word in response_lower)
        return matches / len(expected_words) if expected_words else 0.0
    
    def compare_results(self, raw_results: Dict, holoform_results: Dict) -> Dict[str, Any]:
        """Compare raw code vs Holoform performance"""
        raw_avg_accuracy = sum(test['accuracy'] for test in raw_results['test_results']) / len(raw_results['test_results'])
        holoform_avg_accuracy = sum(test['accuracy'] for test in holoform_results['test_results']) / len(holoform_results['test_results'])
        
        token_reduction = (raw_results['token_count'] - holoform_results['token_count']) / raw_results['token_count']
        
        return {
            "raw_code": {
                "avg_accuracy": raw_avg_accuracy,
                "token_count": raw_results['token_count']
            },
            "holoforms": {
                "avg_accuracy": holoform_avg_accuracy,
                "token_count": holoform_results['token_count']
            },
            "improvements": {
                "accuracy_gain": holoform_avg_accuracy - raw_avg_accuracy,
                "token_reduction": token_reduction,
                "efficiency_score": (holoform_avg_accuracy - raw_avg_accuracy) + token_reduction
            }
        }

def main():
    """CLI entry point"""
    if len(sys.argv) != 3:
        print("Usage: python eval.py <source_file> <holoforms_file>")
        sys.exit(1)
    
    source_file = sys.argv[1]
    holoforms_file = sys.argv[2]
    
    try:
        # Load source code
        with open(source_file, 'r') as f:
            source_code = f.read()
        
        # Load holoforms
        with open(holoforms_file, 'r') as f:
            holoforms = json.load(f)
        
        # Run evaluation
        evaluator = HoloformEvaluator()
        
        print("🧬 Holoform Evaluation")
        print("=" * 50)
        
        print("\n1. Evaluating raw code...")
        raw_results = evaluator.evaluate_raw_code(source_code)
        
        print("2. Evaluating Holoforms...")
        holoform_results = evaluator.evaluate_holoforms(holoforms)
        
        print("3. Comparing results...")
        comparison = evaluator.compare_results(raw_results, holoform_results)
        
        # Print results
        print(f"\nResults:")
        print(f"Raw Code Accuracy: {comparison['raw_code']['avg_accuracy']:.2%}")
        print(f"Holoform Accuracy: {comparison['holoforms']['avg_accuracy']:.2%}")
        print(f"Accuracy Improvement: {comparison['improvements']['accuracy_gain']:.2%}")
        print(f"Token Reduction: {comparison['improvements']['token_reduction']:.2%}")
        print(f"Overall Efficiency Score: {comparison['improvements']['efficiency_score']:.3f}")
        
        # Save detailed results
        with open('evaluation_results.json', 'w') as f:
            json.dump({
                "raw_results": raw_results,
                "holoform_results": holoform_results,
                "comparison": comparison
            }, f, indent=2)
        
        print(f"\n✅ Detailed results saved to evaluation_results.json")
        
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()