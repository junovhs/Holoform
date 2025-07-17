"""
Real World Validation Tests for Computational DNA

This creates rigorous, measurable tests to validate whether AI can:
1. Understand codon patterns
2. Reason correctly about compressed code
3. Answer complex questions accurately
4. Maintain performance across different complexity levels
"""

import json
import tiktoken
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass

def count_tokens(text):
    """Count tokens using GPT-4 tokenizer."""
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))

@dataclass
class ValidationTest:
    """A single validation test with known correct answers."""
    name: str
    scenario: str
    original_rust: str
    codon_dna: str
    question: str
    correct_answer: str
    answer_criteria: List[str]
    difficulty_level: str
    test_dimensions: List[str]

class RealWorldValidator:
    """Creates comprehensive real-world validation tests."""
    
    def __init__(self):
        self.codon_explanation = self._build_codon_explanation()
        self.validation_tests = self._build_validation_tests()
    
    def _build_codon_explanation(self) -> str:
        """Build the explanation of codon system for AI."""
        return """
# Computational DNA: Codon System Explanation

## Core Primitives (4 bases like DNA's ATGC):
- `>` = Flow/Causality ("then", "causes", "leads to")
- `=` = Assignment/Binding ("becomes", "is set to", "equals")
- `?` = Condition/Guard ("if", "when", "test")
- `@` = Context/Scope ("in", "within", "scoped to")

## Key 3-Primitive Patterns (like DNA codons):
- `?>=` = "if condition, then flow to assignment" (conditional set)
- `@>=` = "in context, flow to assignment" (scoped set)
- `>>=` = "flow to assignment" (pipeline result)
- `??>` = "if multiple conditions, then flow" (multi-guard)
- `@?>` = "in context, if condition, then flow" (scoped conditional)
- `@@>` = "in nested contexts, then flow" (nested scope execution)

## Reading Examples:
- `@git>cmd=check>exec?success>=Ok` = "In git context, flow to command equals check, flow to execute, if success then assign Ok"
- `?error>@rollback>=Err` = "If error condition, flow to rollback context and assign Err"
- `@lock>status=active>save?persisted>=Ok` = "In lock context, status becomes active, flow to save, if persisted then assign Ok"

## Context Rules:
- `@context` enters a scope (like with_lock, with_db, in_transaction)
- `>` shows causal flow between operations
- `?condition` tests before proceeding
- `=value` assigns or sets state
"""
    
    def _build_validation_tests(self) -> List[ValidationTest]:
        """Build comprehensive validation tests."""
        
        return [
            # === BASIC COMPREHENSION TESTS ===
            ValidationTest(
                name="Basic Git Operation Understanding",
                scenario="Understanding a simple git command execution pattern",
                original_rust="""
                let mut command = Command::new("git");
                command.arg("apply").arg("--check");
                let output = command.spawn()?.wait_with_output()?;
                if output.status.success() {
                    Ok(())
                } else {
                    Err(PatchError::Validation(String::from_utf8_lossy(&output.stderr).to_string()))
                }
                """,
                codon_dna="@git>cmd=check>exec?success>=Ok?!success>=Err",
                question="What happens if the git command fails?",
                correct_answer="If the git command fails (!success), then an Err is returned with validation error details",
                answer_criteria=[
                    "Must mention that failure leads to Err",
                    "Must understand the !success condition",
                    "Should recognize this is error handling"
                ],
                difficulty_level="Basic",
                test_dimensions=["Comprehension", "Error Handling", "Conditional Logic"]
            ),
            
            ValidationTest(
                name="Context Scoping Logic",
                scenario="Understanding nested context operations",
                original_rust="""
                with_transaction(|| {
                    with_lock(|| {
                        user.status = Status::Active;
                        user.save()?;
                        if user.is_persisted() {
                            notify_user(&user);
                            Ok(user)
                        } else {
                            Err(PersistenceError::SaveFailed)
                        }
                    })
                })
                """,
                codon_dna="@transaction>@lock>status=active>save?persisted>notify>=Ok?!persisted>=Err",
                question="In what order do the operations execute, and what contexts are they in?",
                correct_answer="1) Enter transaction context, 2) Enter lock context, 3) Set status to active, 4) Save user, 5) If persisted: notify user then return Ok, 6) If not persisted: return Err",
                answer_criteria=[
                    "Must identify the nested context order (transaction -> lock)",
                    "Must list operations in correct sequence",
                    "Must understand conditional branching at the end",
                    "Should recognize the scoped nature of operations"
                ],
                difficulty_level="Intermediate",
                test_dimensions=["Context Understanding", "Sequential Logic", "Nested Scopes", "Conditional Branching"]
            ),
            
            # === REASONING TESTS ===
            ValidationTest(
                name="Error Recovery Flow Tracing",
                scenario="Tracing complex error recovery with rollback",
                original_rust="""
                match apply_patch(patch_content, repo_path) {
                    Ok(success) => {
                        run_tests(repo_path)?;
                        Ok(success)
                    },
                    Err(patch_error) => {
                        rollback_changes(repo_path)?;
                        log_error(&patch_error);
                        cleanup_temp_files()?;
                        Err(patch_error)
                    }
                }
                """,
                codon_dna="?patch_ok>run_tests>=Ok?patch_err>@rollback>log>cleanup>=Err",
                question="If patch application fails, what is the complete sequence of recovery operations?",
                correct_answer="If patch fails: 1) Enter rollback context, 2) Log the error, 3) Cleanup temp files, 4) Return the original error",
                answer_criteria=[
                    "Must identify all 4 recovery steps in correct order",
                    "Must understand this only happens on patch failure",
                    "Should recognize the rollback context grouping",
                    "Must mention that original error is preserved and returned"
                ],
                difficulty_level="Advanced",
                test_dimensions=["Error Recovery", "Sequential Logic", "Context Scoping", "State Management"]
            ),
            
            ValidationTest(
                name="Multi-Condition Decision Tree",
                scenario="Complex conditional logic with multiple paths",
                original_rust="""
                if user.is_authenticated() && user.has_permission("write") && !repo.is_locked() {
                    if backup_exists(&repo.path) {
                        apply_changes(&repo, &changes)?;
                        Ok(ChangeResult::Applied)
                    } else {
                        create_backup(&repo)?;
                        apply_changes(&repo, &changes)?;
                        Ok(ChangeResult::AppliedWithBackup)
                    }
                } else {
                    Err(PermissionError::AccessDenied)
                }
                """,
                codon_dna="?auth&&write&&!locked>?backup>apply>=Applied?!backup>create_backup>apply>=AppliedWithBackup?!auth||!write||locked>=AccessDenied",
                question="Under what conditions will changes be applied WITH backup creation?",
                correct_answer="Changes are applied WITH backup creation when: user is authenticated AND has write permission AND repo is not locked AND backup does NOT exist",
                answer_criteria=[
                    "Must identify all 4 required conditions (auth, write, !locked, !backup)",
                    "Must understand this is specifically for the backup creation path",
                    "Should recognize the logical AND relationship between conditions",
                    "Must distinguish from the regular apply path"
                ],
                difficulty_level="Advanced",
                test_dimensions=["Complex Conditionals", "Logical Operators", "Decision Trees", "State Analysis"]
            ),
            
            # === PERFORMANCE TESTS ===
            ValidationTest(
                name="Resource Management Pattern",
                scenario="Understanding resource acquisition and cleanup patterns",
                original_rust="""
                let file = File::open(&config_path)?;
                let mut reader = BufReader::new(file);
                let mut content = String::new();
                reader.read_to_string(&mut content)?;
                
                let parsed_config = parse_config(&content)?;
                validate_config(&parsed_config)?;
                
                if parsed_config.requires_backup {
                    create_backup(&parsed_config.backup_path)?;
                }
                
                apply_config(parsed_config)
                """,
                codon_dna="@file>open>=reader>read>=content>parse>=config>validate?backup_required>create_backup>apply",
                question="What happens if config validation fails?",
                correct_answer="If config validation fails, the process stops at the validate step and returns an error - no backup is created and config is not applied",
                answer_criteria=[
                    "Must understand that validation failure stops the flow",
                    "Must recognize that subsequent steps (backup, apply) don't execute",
                    "Should understand the sequential dependency",
                    "Must mention error propagation"
                ],
                difficulty_level="Intermediate",
                test_dimensions=["Resource Management", "Error Propagation", "Sequential Dependencies", "Flow Control"]
            ),
            
            # === EDGE CASE TESTS ===
            ValidationTest(
                name="Concurrent Context Handling",
                scenario="Understanding concurrent operations with shared state",
                original_rust="""
                let results = Arc::new(Mutex::new(Vec::new()));
                let handles: Vec<_> = tasks.into_iter().map(|task| {
                    let results_clone = Arc::clone(&results);
                    thread::spawn(move || {
                        match process_task(task) {
                            Ok(result) => {
                                let mut results_guard = results_clone.lock().unwrap();
                                results_guard.push(result);
                            },
                            Err(e) => {
                                log_error(&e);
                            }
                        }
                    })
                }).collect();
                
                for handle in handles {
                    handle.join().unwrap();
                }
                """,
                codon_dna="@concurrent>@tasks>process?success>@lock>results.push?error>log@join>wait",
                question="How is shared state (results) protected in this concurrent scenario?",
                correct_answer="Shared state is protected by using a lock (@lock) - each thread must acquire the lock before pushing results, ensuring thread-safe access to the shared Vec",
                answer_criteria=[
                    "Must identify the lock mechanism for protection",
                    "Must understand this prevents race conditions",
                    "Should recognize the concurrent context",
                    "Must mention thread-safe access"
                ],
                difficulty_level="Advanced",
                test_dimensions=["Concurrency", "Shared State", "Thread Safety", "Context Management"]
            ),
            
            # === INTEGRATION TESTS ===
            ValidationTest(
                name="Full CLI Operation Simulation",
                scenario="Complete CLI operation with validation, execution, and cleanup",
                original_rust="""
                // Validate input
                let patch = validate_patch_format(&input)?;
                
                // Check repository state
                if !repo.is_clean() {
                    return Err(RepoError::DirtyWorkingDirectory);
                }
                
                // Create backup
                let backup_path = create_backup(&repo)?;
                
                // Apply patch with rollback on failure
                match apply_patch(&patch, &repo) {
                    Ok(_) => {
                        // Run tests
                        match run_tests(&repo) {
                            Ok(_) => {
                                cleanup_backup(&backup_path)?;
                                Ok(PatchResult::Success)
                            },
                            Err(test_error) => {
                                rollback_from_backup(&backup_path, &repo)?;
                                Err(PatchError::TestsFailed(test_error))
                            }
                        }
                    },
                    Err(patch_error) => {
                        rollback_from_backup(&backup_path, &repo)?;
                        Err(patch_error)
                    }
                }
                """,
                codon_dna="validate>=patch?!clean>=DirtyRepo>create_backup>=backup_path?patch_ok>?tests_ok>cleanup>=Success?tests_fail>@rollback>=TestsFailed?patch_fail>@rollback>=PatchError",
                question="If patch application succeeds but tests fail, what is the complete recovery sequence?",
                correct_answer="If patch succeeds but tests fail: 1) Enter rollback context, 2) Restore from backup, 3) Return TestsFailed error with the test error details",
                answer_criteria=[
                    "Must identify that patch succeeded initially",
                    "Must recognize test failure triggers rollback",
                    "Must mention backup restoration",
                    "Must identify correct error type (TestsFailed)",
                    "Should understand the conditional flow"
                ],
                difficulty_level="Expert",
                test_dimensions=["Integration Flow", "Error Recovery", "State Management", "Complex Conditionals", "Resource Cleanup"]
            )
        ]
    
    def generate_test_prompts(self) -> Dict[str, Any]:
        """Generate the complete test prompts for AI validation."""
        
        test_prompts = {
            "explanation": self.codon_explanation,
            "tests": []
        }
        
        for test in self.validation_tests:
            # Create the test prompt
            prompt = f"""
# Real World Validation Test: {test.name}

## Scenario
{test.scenario}

## Original Rust Code ({count_tokens(test.original_rust)} tokens)
```rust
{test.original_rust.strip()}
```

## Codon DNA Representation ({count_tokens(test.codon_dna)} tokens)
```
{test.codon_dna}
```

## Question
{test.question}

## Instructions
Please analyze the Codon DNA representation and provide a detailed answer. Focus on accuracy and completeness.
"""
            
            # Calculate compression metrics
            original_tokens = count_tokens(test.original_rust)
            codon_tokens = count_tokens(test.codon_dna)
            compression_ratio = (original_tokens - codon_tokens) / original_tokens * 100
            
            test_data = {
                "name": test.name,
                "difficulty": test.difficulty_level,
                "dimensions": test.test_dimensions,
                "prompt": prompt,
                "correct_answer": test.correct_answer,
                "answer_criteria": test.answer_criteria,
                "metrics": {
                    "original_tokens": original_tokens,
                    "codon_tokens": codon_tokens,
                    "compression_ratio": compression_ratio
                }
            }
            
            test_prompts["tests"].append(test_data)
        
        return test_prompts
    
    def create_comprehensive_test_suite(self):
        """Create the complete test suite for real-world validation."""
        
        print("🧬 REAL WORLD VALIDATION TEST SUITE")
        print("=" * 80)
        print("Creating comprehensive tests to validate Computational DNA system")
        print()
        
        # Generate all test prompts
        test_suite = self.generate_test_prompts()
        
        # Show test overview
        print("📊 TEST SUITE OVERVIEW")
        print("-" * 40)
        
        difficulty_counts = {}
        dimension_counts = {}
        total_compression = 0
        
        for test in test_suite["tests"]:
            # Count by difficulty
            diff = test["difficulty"]
            difficulty_counts[diff] = difficulty_counts.get(diff, 0) + 1
            
            # Count by dimensions
            for dim in test["dimensions"]:
                dimension_counts[dim] = dimension_counts.get(dim, 0) + 1
            
            # Track compression
            total_compression += test["metrics"]["compression_ratio"]
        
        print(f"Total Tests: {len(test_suite['tests'])}")
        print(f"Average Compression: {total_compression / len(test_suite['tests']):.1f}%")
        print()
        
        print("By Difficulty:")
        for diff, count in difficulty_counts.items():
            print(f"  {diff}: {count} tests")
        print()
        
        print("By Test Dimensions:")
        for dim, count in sorted(dimension_counts.items()):
            print(f"  {dim}: {count} tests")
        print()
        
        # Show individual tests
        print("🧪 INDIVIDUAL TESTS")
        print("=" * 80)
        
        for i, test in enumerate(test_suite["tests"], 1):
            print(f"TEST {i}: {test['name']}")
            print(f"Difficulty: {test['difficulty']}")
            print(f"Dimensions: {', '.join(test['dimensions'])}")
            print(f"Compression: {test['metrics']['compression_ratio']:.1f}% ({test['metrics']['original_tokens']} → {test['metrics']['codon_tokens']} tokens)")
            print()
            print("PROMPT TO COPY:")
            print("-" * 40)
            print(test_suite["explanation"])
            print(test["prompt"])
            print()
            print("CORRECT ANSWER:")
            print(test["correct_answer"])
            print()
            print("VALIDATION CRITERIA:")
            for criterion in test["answer_criteria"]:
                print(f"  ✓ {criterion}")
            print()
            print("=" * 80)
            print()
        
        # Save to file
        with open("real_world_validation_tests.json", "w") as f:
            json.dump(test_suite, f, indent=2)
        
        print("💾 COMPLETE TEST SUITE SAVED")
        print("File: real_world_validation_tests.json")
        print()
        print("🎯 TESTING INSTRUCTIONS")
        print("=" * 40)
        print("1. Copy the explanation + each test prompt to an AI (ChatGPT, Claude, etc.)")
        print("2. Compare AI answers to the correct answers provided")
        print("3. Check each answer against the validation criteria")
        print("4. Score: ✓ Pass if meets all criteria, ✗ Fail if missing key points")
        print("5. Track results across difficulty levels and test dimensions")
        print()
        print("🏆 SUCCESS METRICS")
        print("=" * 40)
        print("- Basic tests: Should achieve 90%+ pass rate")
        print("- Intermediate tests: Should achieve 80%+ pass rate") 
        print("- Advanced tests: Should achieve 70%+ pass rate")
        print("- Expert tests: Should achieve 60%+ pass rate")
        print()
        print("If these thresholds are met, Computational DNA is VALIDATED! 🧬")

def main():
    """Run the real world validation test generator."""
    validator = RealWorldValidator()
    validator.create_comprehensive_test_suite()

if __name__ == "__main__":
    main()