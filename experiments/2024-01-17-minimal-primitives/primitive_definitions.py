"""
Minimal Primitives for HoloChain: DNA-Inspired Computational Atoms

This module defines the minimal set of primitives that can combine
to represent any computational behavior, inspired by DNA's 4-base system.
"""

import tiktoken
from typing import Dict, List, Tuple
from dataclasses import dataclass

def count_tokens(text):
    """Count tokens using GPT-4 tokenizer."""
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))

@dataclass
class Primitive:
    """A single computational primitive."""
    symbol: str
    name: str
    meaning: str
    examples: List[str]

class MinimalPrimitiveSystem:
    """The minimal primitive system for computational representation."""
    
    def __init__(self):
        # Define the 4 core primitives (like DNA's ATGC)
        self.primitives = {
            '>': Primitive(
                symbol='>',
                name='Flow',
                meaning='Causality, sequence, data flow, "then"',
                examples=['a>b (a causes b)', 'input>process>output', 'validate>execute']
            ),
            '=': Primitive(
                symbol='=',
                name='Bind',
                meaning='Assignment, transformation, "becomes"',
                examples=['x=5', 'status=valid', 'result=processed']
            ),
            '?': Primitive(
                symbol='?',
                name='Guard',
                meaning='Condition, test, "if"',
                examples=['?valid', '?x>5', '?error']
            ),
            '@': Primitive(
                symbol='@',
                name='Context',
                meaning='Scope, location, "in/at"',
                examples=['@auth', '@database', '@error_handler']
            )
        }
        
        # Pre-compute all 2-primitive combinations (16 total)
        self.two_primitive_patterns = self._generate_two_primitive_patterns()
        
        # Pre-compute all 3-primitive combinations (64 total, like DNA codons)
        self.three_primitive_patterns = self._generate_three_primitive_patterns()
    
    def _generate_two_primitive_patterns(self) -> Dict[str, str]:
        """Generate all 16 two-primitive combinations."""
        symbols = list(self.primitives.keys())
        patterns = {}
        
        for first in symbols:
            for second in symbols:
                combo = first + second
                patterns[combo] = self._interpret_two_primitive(first, second)
        
        return patterns
    
    def _interpret_two_primitive(self, first: str, second: str) -> str:
        """Interpret the meaning of a two-primitive combination."""
        meanings = {
            '>=': 'flow-to-assignment (pipeline)',
            '>?': 'flow-to-condition (test result)',
            '>@': 'flow-to-context (enter scope)',
            '=>': 'assign-then-flow (set and continue)',
            '=?': 'assign-then-test (set and check)',
            '=@': 'assign-to-context (set in scope)',
            '?>': 'condition-then-flow (guarded execution)',
            '?=': 'condition-then-assign (conditional set)',
            '?@': 'condition-in-context (scoped guard)',
            '@>': 'context-then-flow (scoped execution)',
            '@=': 'context-then-assign (scoped set)',
            '@?': 'context-then-condition (scoped test)',
            '>>': 'sequential-flow (pipeline)',
            '==': 'equality-test (comparison)',
            '??': 'conditional-chain (nested if)',
            '@@': 'context-nesting (scope hierarchy)'
        }
        
        return meanings.get(first + second, f'{first}-then-{second}')
    
    def _generate_three_primitive_patterns(self) -> Dict[str, str]:
        """Generate all 64 three-primitive combinations (like DNA codons)."""
        symbols = list(self.primitives.keys())
        patterns = {}
        
        for first in symbols:
            for second in symbols:
                for third in symbols:
                    combo = first + second + third
                    patterns[combo] = self._interpret_three_primitive(first, second, third)
        
        return patterns
    
    def _interpret_three_primitive(self, first: str, second: str, third: str) -> str:
        """Interpret the meaning of a three-primitive combination."""
        # Some key patterns (like DNA's most important codons)
        key_patterns = {
            '?>=': 'if-condition-then-flow-to-assignment (conditional pipeline)',
            '@?>': 'in-context-if-condition-then-flow (scoped conditional)',
            '>=@': 'flow-to-assignment-in-context (scoped pipeline)',
            '?@>': 'if-context-condition-then-flow (context-dependent execution)',
            '>?=': 'flow-then-test-then-assign (validate-and-set)',
            '=?>': 'assign-then-test-then-flow (set-validate-continue)',
            '@>=': 'in-context-flow-to-assignment (scoped transformation)',
            '?=@': 'if-condition-assign-to-context (conditional context-set)',
            '>@?': 'flow-to-context-then-test (enter-scope-and-validate)',
            '=@>': 'assign-to-context-then-flow (set-context-and-continue)',
        }
        
        combo = first + second + third
        return key_patterns.get(combo, f'{first}-{second}-{third} pattern')

def test_primitive_compression():
    """Test compression using minimal primitives."""
    
    system = MinimalPrimitiveSystem()
    
    # Test cases: original code vs minimal primitive representation
    test_cases = [
        {
            'name': 'Simple Validation',
            'original': 'if user.email: user.status = "valid"',
            'primitive': '?email>=status=valid',
            'meaning': 'if email exists, then flow to assign status as valid'
        },
        {
            'name': 'Context-Scoped Operation',
            'original': 'with database_context: if record.exists(): record.update(data)',
            'primitive': '@db?exists>=update',
            'meaning': 'in database context, if exists condition, then flow to update'
        },
        {
            'name': 'Error Handling',
            'original': 'try: process_data() except: rollback(); raise_error()',
            'primitive': '?error>@rollback>=raise',
            'meaning': 'if error condition, flow to rollback context and assign raise'
        },
        {
            'name': 'Authentication Flow',
            'original': 'if authenticate(token): user = get_user(token); return success',
            'primitive': '@auth?token>=user>success',
            'meaning': 'in auth context, if token valid, assign user then flow to success'
        },
        {
            'name': 'Your Rust Patch Function',
            'original': '''
            let mut command = Command::new("git");
            command.arg("apply").arg("--check");
            let output = command.output()?;
            if output.status.success() { Ok(()) } else { Err(error) }
            ''',
            'primitive': '@git>cmd=apply>exec?success>=Ok?!success>=Err',
            'meaning': 'in git context, flow to command equals apply, flow to execute, if success assign Ok, if not success assign Err'
        }
    ]
    
    print("=== Minimal Primitive Compression Test ===")
    print(f"Using 4 primitives: {list(system.primitives.keys())}")
    print("=" * 60)
    
    total_original_tokens = 0
    total_primitive_tokens = 0
    
    for case in test_cases:
        original_tokens = count_tokens(case['original'])
        primitive_tokens = count_tokens(case['primitive'])
        compression = (original_tokens - primitive_tokens) / original_tokens * 100
        
        total_original_tokens += original_tokens
        total_primitive_tokens += primitive_tokens
        
        print(f"Test: {case['name']}")
        print(f"Original ({original_tokens} tokens): {case['original']}")
        print(f"Primitive ({primitive_tokens} tokens): {case['primitive']}")
        print(f"Meaning: {case['meaning']}")
        print(f"Compression: {compression:.1f}%")
        print()
    
    overall_compression = (total_original_tokens - total_primitive_tokens) / total_original_tokens * 100
    print(f"=== Overall Results ===")
    print(f"Total Original Tokens: {total_original_tokens}")
    print(f"Total Primitive Tokens: {total_primitive_tokens}")
    print(f"Overall Compression: {overall_compression:.1f}%")
    
    # Show the combinatorial power
    print(f"\n=== Combinatorial Power ===")
    print(f"4 primitives = 4 meanings")
    print(f"2-primitive combinations = 16 patterns")
    print(f"3-primitive combinations = 64 patterns (like DNA codons)")
    print(f"4-primitive combinations = 256 patterns")
    print(f"5+ primitives = infinite complexity")
    
    print(f"\n=== Sample 3-Primitive Patterns (DNA Codons) ===")
    for i, (pattern, meaning) in enumerate(list(system.three_primitive_patterns.items())[:10]):
        print(f"  {pattern}: {meaning}")
    print(f"  ... and {len(system.three_primitive_patterns) - 10} more patterns")

def analyze_your_cli_with_primitives():
    """Analyze how your CLI patterns could be represented with minimal primitives."""
    
    print("\n=== Your CLI Analysis with Minimal Primitives ===")
    
    # Your CLI patterns mapped to primitives
    cli_patterns = {
        'Patch Validation': {
            'rust_code': 'Command::new("git").arg("apply").arg("--check").output()',
            'primitive': '@git>cmd=check>exec',
            'tokens_saved': '~70%'
        },
        'Error Recovery': {
            'rust_code': 'if let Err(e) = result { rollback(); return Err(e); }',
            'primitive': '?err>@rollback>=Err',
            'tokens_saved': '~75%'
        },
        'State Modification': {
            'rust_code': 'user.status = Status::Invalid; user.login_count = 0;',
            'primitive': 'status=invalid>count=0',
            'tokens_saved': '~60%'
        },
        'Resource Management': {
            'rust_code': 'let file = File::open(path)?; let content = file.read()?;',
            'primitive': '@file>open>=content',
            'tokens_saved': '~65%'
        }
    }
    
    for pattern_name, data in cli_patterns.items():
        print(f"{pattern_name}:")
        print(f"  Rust: {data['rust_code']}")
        print(f"  Primitive: {data['primitive']}")
        print(f"  Estimated compression: {data['tokens_saved']}")
        print()
    
    print("🎯 Key Insight: Your CLI's repetitive patterns (git commands, error handling,")
    print("   file operations) could compress extremely well with minimal primitives!")

if __name__ == "__main__":
    test_primitive_compression()
    analyze_your_cli_with_primitives()