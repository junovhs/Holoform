"""
Manual Testing Framework for Codon Validation

This framework generates test cases for manual validation with AI chat models.
Each test is designed to be copy-pasted into ChatGPT, Claude, or Gemini
for systematic validation of codon comprehension.

Date: July 18, 2025
Phase: Codon Refinement and Validation
"""

from codon_library_v2 import RefinedComputationalDNA, CodonCategory
from typing import Dict, List, Tuple
import json
import random

class ManualTestGenerator:
    """Generates manual test cases for AI model validation."""
    
    def __init__(self):
        self.dna = RefinedComputationalDNA()
        self.test_counter = 1
        
    def generate_single_codon_test(self, pattern: str, difficulty: str = "intermediate") -> Dict:
        """Generate a single codon test for manual validation."""
        
        codon = self.dna.get_codon_by_pattern(pattern)
        if not codon:
            return {}
        
        test_id = f"TEST-{self.test_counter:03d}"
        self.test_counter += 1
        
        # Create test based on difficulty
        if difficulty == "basic":
            return self._create_basic_test(test_id, codon)
        elif difficulty == "intermediate":
            return self._create_intermediate_test(test_id, codon)
        elif difficulty == "advanced":
            return self._create_advanced_test(test_id, codon)
        elif difficulty == "expert":
            return self._create_expert_test(test_id, codon)
    
    def _create_basic_test(self, test_id: str, codon) -> Dict:
        """Create basic comprehension test."""
        
        return {
            'test_id': test_id,
            'difficulty': 'Basic',
            'pattern': codon.pattern,
            'category': codon.category.value,
            'prompt_for_ai': f"""
I'm testing a computational notation system. Please analyze this pattern:

**Pattern:** {codon.pattern}

**Question:** What computational behavior does this pattern represent?

Please explain:
1. What type of operation this represents
2. The sequence of execution
3. Any conditions or requirements

Do not ask for additional context - analyze based solely on the pattern.
            """.strip(),
            'validation_criteria': [
                f"Must identify this as {codon.category.value.lower()}",
                f"Must mention '{codon.name.lower().replace('-', ' ')}'",
                "Must describe execution sequence",
                "Should not request additional context"
            ],
            'expected_keywords': [
                codon.name.lower().split('-')[0],
                'execution' if '>' in codon.pattern else 'condition' if '?' in codon.pattern else 'assignment' if '=' in codon.pattern else 'context',
                'sequential' if '>>' in codon.pattern else 'conditional' if '??' in codon.pattern else 'scoped' if '@@' in codon.pattern else 'flow'
            ],
            'internal_notes': {
                'precise_meaning': codon.precise_meaning,
                'compression_power': codon.compression_power,
                'ai_score_target': codon.ai_comprehension_score
            }
        }
    
    def _create_intermediate_test(self, test_id: str, codon) -> Dict:
        """Create intermediate comprehension test with context."""
        
        # Select a representative example
        example_code = codon.rust_examples[0] if codon.rust_examples else ""
        
        return {
            'test_id': test_id,
            'difficulty': 'Intermediate',
            'pattern': codon.pattern,
            'category': codon.category.value,
            'prompt_for_ai': f"""
I'm testing a computational DNA notation system where code is compressed into symbolic patterns.

**Codon Pattern:** {codon.pattern}

**Question:** Given this codon pattern, what is the complete execution flow?

Please provide:
1. Step-by-step execution order
2. What conditions must be met (if any)
3. What gets assigned or modified (if any)
4. What context or scope is involved (if any)
5. How errors would be handled

Analyze based solely on the codon pattern - do not ask for the original code.
            """.strip(),
            'validation_criteria': [
                "Must describe step-by-step execution",
                "Must identify conditions correctly" if '?' in codon.pattern else "Must identify assignments correctly" if '=' in codon.pattern else "Must identify context correctly" if '@' in codon.pattern else "Must identify flow correctly",
                f"Must understand {codon.category.value.lower()} behavior",
                "Should mention error handling" if codon.error_handling else "Should handle missing error info gracefully",
                "Must not request original code"
            ],
            'expected_keywords': [
                'step', 'order', 'sequence',
                'condition' if '?' in codon.pattern else 'assign' if '=' in codon.pattern else 'context' if '@' in codon.pattern else 'flow',
                'error' if codon.error_handling else 'execution'
            ],
            'internal_notes': {
                'precise_meaning': codon.precise_meaning,
                'error_handling': codon.error_handling or "No explicit error handling defined",
                'example_code': example_code,
                'compression_ratio': f"{((len(example_code) - len(codon.pattern)) / len(example_code) * 100):.1f}%" if example_code else "N/A"
            }
        }
    
    def _create_advanced_test(self, test_id: str, codon) -> Dict:
        """Create advanced test with complex scenarios."""
        
        # Create a complex scenario using the codon
        scenario = self._generate_complex_scenario(codon)
        
        return {
            'test_id': test_id,
            'difficulty': 'Advanced',
            'pattern': codon.pattern,
            'category': codon.category.value,
            'prompt_for_ai': f"""
Advanced Computational DNA Analysis

**Codon Sequence:** {scenario['codon_sequence']}

**Scenario:** {scenario['description']}

**Question:** {scenario['question']}

Please analyze:
1. The complete execution path
2. All decision points and their outcomes
3. Resource management and cleanup
4. Error propagation and recovery
5. Performance implications

Base your analysis entirely on the codon sequence provided.
            """.strip(),
            'validation_criteria': [
                "Must trace complete execution path",
                "Must identify all decision points",
                "Must understand resource implications",
                "Must address error scenarios",
                "Should discuss performance considerations"
            ],
            'expected_keywords': [
                'execution', 'path', 'decision',
                'resource', 'cleanup', 'error',
                'performance', 'optimization'
            ],
            'internal_notes': {
                'scenario': scenario,
                'complexity_level': 'Advanced',
                'multi_codon': len(scenario['codon_sequence'].split()) > 1
            }
        }
    
    def _create_expert_test(self, test_id: str, codon) -> Dict:
        """Create expert-level test with real-world complexity."""
        
        # Create a real-world system scenario
        system_scenario = self._generate_system_scenario(codon)
        
        return {
            'test_id': test_id,
            'difficulty': 'Expert',
            'pattern': codon.pattern,
            'category': codon.category.value,
            'prompt_for_ai': f"""
Expert-Level System Analysis

**System Codon Chain:** {system_scenario['codon_chain']}

**Context:** {system_scenario['system_context']}

**Critical Question:** {system_scenario['critical_question']}

**Analysis Required:**
1. Complete system behavior prediction
2. Failure mode analysis
3. Concurrency and race condition implications
4. Resource lifecycle management
5. Security and data integrity considerations
6. Scalability bottlenecks

Provide a comprehensive analysis based solely on the codon representation.
            """.strip(),
            'validation_criteria': [
                "Must predict complete system behavior",
                "Must identify potential failure modes",
                "Must address concurrency concerns",
                "Must discuss resource lifecycle",
                "Should identify security implications",
                "Should analyze scalability factors"
            ],
            'expected_keywords': [
                'system', 'behavior', 'failure',
                'concurrency', 'race', 'resource',
                'security', 'scalability', 'integrity'
            ],
            'internal_notes': {
                'system_scenario': system_scenario,
                'complexity_level': 'Expert',
                'real_world_applicable': True
            }
        }
    
    def _generate_complex_scenario(self, codon) -> Dict:
        """Generate complex scenario for advanced testing."""
        
        scenarios = {
            '>>=': {
                'codon_sequence': '?auth>>=user @db?exists>=record >>=result',
                'description': 'User authentication and data retrieval system',
                'question': 'If authentication succeeds but the database record doesn\'t exist, what is the complete execution path and final state?'
            },
            '?>=': {
                'codon_sequence': '?valid>=process ?error>!~rollback',
                'description': 'Data validation with error recovery',
                'question': 'What happens if validation fails, and how does the error recovery mechanism work?'
            },
            '@>=': {
                'codon_sequence': '@lock>=counter @transaction>=save ?success>notify',
                'description': 'Thread-safe counter increment with persistence',
                'question': 'How are race conditions prevented, and what happens if the transaction fails?'
            }
        }
        
        return scenarios.get(codon.pattern, {
            'codon_sequence': codon.pattern,
            'description': f'Generic {codon.category.value.lower()} scenario',
            'question': f'How does the {codon.name.lower()} pattern behave in this context?'
        })
    
    def _generate_system_scenario(self, codon) -> Dict:
        """Generate system-level scenario for expert testing."""
        
        system_scenarios = {
            '>>=': {
                'codon_chain': '@auth?token>>=user @cache?hit>=data @db?miss>=fetch @cache>=store >>=response',
                'system_context': 'High-traffic web API with authentication, caching, and database layers',
                'critical_question': 'Under high concurrent load, what are the potential race conditions and how does the system maintain data consistency?'
            },
            '?>=': {
                'codon_chain': '?rate_limit>=reject ?auth>=proceed @db?available>=query ?timeout>!~circuit_breaker',
                'system_context': 'Distributed microservice with rate limiting, authentication, and circuit breaker pattern',
                'critical_question': 'How does the system handle cascading failures when the database becomes unavailable?'
            },
            '@>=': {
                'codon_chain': '@transaction>@lock>=update @audit>=log @notification>=send ?failure>!~compensate',
                'system_context': 'Financial transaction processing system with audit trail and compensation logic',
                'critical_question': 'What guarantees does this system provide for data consistency and how are partial failures handled?'
            }
        }
        
        return system_scenarios.get(codon.pattern, {
            'codon_chain': f'{codon.pattern} @system>=state',
            'system_context': f'Generic system using {codon.category.value.lower()} patterns',
            'critical_question': f'How does the {codon.name.lower()} pattern affect system reliability and performance?'
        })
    
    def generate_test_suite(self, patterns: List[str], difficulty: str = "intermediate") -> List[Dict]:
        """Generate a complete test suite for multiple patterns."""
        
        test_suite = []
        for pattern in patterns:
            test = self.generate_single_codon_test(pattern, difficulty)
            if test:
                test_suite.append(test)
        
        return test_suite
    
    def export_test_for_ai_chat(self, test: Dict) -> str:
        """Export test in format ready for AI chat."""
        
        return f"""
=== CODON VALIDATION TEST {test['test_id']} ===
Difficulty: {test['difficulty']}
Category: {test['category']}

{test['prompt_for_ai']}

=== END TEST ===
        """.strip()
    
    def create_validation_checklist(self, test: Dict) -> str:
        """Create validation checklist for manual scoring."""
        
        checklist = f"""
=== VALIDATION CHECKLIST - {test['test_id']} ===

Pattern: {test['pattern']}
Difficulty: {test['difficulty']}

CRITERIA (Check each):
"""
        
        for i, criterion in enumerate(test['validation_criteria'], 1):
            checklist += f"[ ] {i}. {criterion}\n"
        
        checklist += f"""
EXPECTED KEYWORDS (Should mention):
{', '.join(test['expected_keywords'])}

SCORING:
- All criteria met: PASS (100%)
- 80%+ criteria met: STRONG PASS (80-99%)
- 60-79% criteria met: WEAK PASS (60-79%)
- <60% criteria met: FAIL (<60%)

NOTES:
_________________________________
_________________________________
_________________________________

FINAL SCORE: _____ / {len(test['validation_criteria'])} = _____%
RESULT: [ ] PASS [ ] STRONG PASS [ ] WEAK PASS [ ] FAIL
        """
        
        return checklist

def generate_priority_test_suite():
    """Generate test suite for priority codons."""
    
    print("=== Generating Priority Codon Test Suite ===")
    print("Date: July 18, 2025")
    print("Phase: Manual Validation Testing")
    print("=" * 50)
    
    generator = ManualTestGenerator()
    
    # Priority patterns from refined library
    priority_patterns = [
        '>>=',  # Pipeline-Assignment
        '?>=',  # Conditional-Pipeline-Assignment
        '@>=',  # Scoped-Pipeline-Assignment
        '??>',  # Multi-Guard-Execution
        '??=',  # Multi-Guard-Assignment
    ]
    
    # Generate tests for each difficulty level
    difficulties = ['basic', 'intermediate', 'advanced']
    
    all_tests = []
    
    for difficulty in difficulties:
        print(f"\n=== {difficulty.upper()} TESTS ===")
        
        for pattern in priority_patterns:
            test = generator.generate_single_codon_test(pattern, difficulty)
            if test:
                all_tests.append(test)
                print(f"Generated {test['test_id']}: {pattern} ({difficulty})")
    
    print(f"\nTotal tests generated: {len(all_tests)}")
    
    # Export first few tests as examples
    print("\n=== SAMPLE TEST FOR AI CHAT ===")
    if all_tests:
        sample_test = all_tests[0]
        print(generator.export_test_for_ai_chat(sample_test))
        
        print("\n=== SAMPLE VALIDATION CHECKLIST ===")
        print(generator.create_validation_checklist(sample_test))
    
    return all_tests

if __name__ == "__main__":
    generate_priority_test_suite()