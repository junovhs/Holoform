# Design Document: Finding the Holoform Magic Moment

## Overview

This experiment is designed to discover concrete evidence that Holoforms provide unique value for AI code understanding. We'll conduct focused comparative tests to identify specific scenarios where Holoforms enable superior AI comprehension compared to raw source code or other representations.

## Architecture

### Experiment Framework

The experiment consists of three main components:

1. **Test Case Generator**: Creates diverse code examples with known "ground truth" answers
2. **Representation Converter**: Transforms code into different formats (raw, Holoform, AST)
3. **LLM Evaluator**: Presents tasks to LLMs and collects responses
4. **Response Analyzer**: Objectively scores and compares LLM responses

### Test Case Categories

#### Category 1: Inter-Function Data Flow
Code examples where understanding requires tracing data flow across multiple functions:

```python
# Example: Hidden state modification
def process_user_data(user_id):
    user = get_user(user_id)
    validate_user(user)
    update_user_stats(user)
    return user

def validate_user(user):
    if not user.email:
        user.status = "invalid"  # Hidden side effect
    
def update_user_stats(user):
    if user.status == "invalid":
        user.login_count = 0  # Depends on hidden modification
```

**Test Question**: "What happens to a user's login_count if they don't have an email?"

**Expected Insight**: The LLM should trace the data flow: missing email → status set to "invalid" → login_count reset to 0.

#### Category 2: Complex Control Flow
Code with nested conditions and loops that create non-obvious execution paths:

```python
def analyze_data(items):
    results = []
    for item in items:
        if item.type == "critical":
            if process_critical(item):
                results.append(item)
                continue
        elif item.type == "normal":
            if item.priority > 5:
                results.append(transform_item(item))
            else:
                skip_item(item)
    return results
```

**Test Question**: "Under what conditions will an item be added to results?"

**Expected Insight**: The LLM should identify all execution paths that lead to items being added to results.

#### Category 3: Cross-File Dependencies
Multi-file scenarios where understanding requires knowledge of call relationships:

```python
# file1.py
def main():
    data = load_config()
    processor = DataProcessor(data)
    return processor.run()

# file2.py  
class DataProcessor:
    def __init__(self, config):
        self.validator = create_validator(config.validation_rules)
    
    def run(self):
        # Implementation depends on validator created in __init__
        pass

# file3.py
def create_validator(rules):
    # Returns different validators based on rules
    pass
```

**Test Question**: "How does the validation_rules configuration affect the behavior of DataProcessor.run()?"

## Components and Interfaces

### Test Case Generator

```python
class TestCaseGenerator:
    def __init__(self):
        self.categories = [
            InterFunctionDataFlow(),
            ComplexControlFlow(), 
            CrossFileDependencies()
        ]
    
    def generate_test_cases(self, num_cases_per_category=5):
        """Generate test cases across all categories."""
        test_cases = []
        for category in self.categories:
            cases = category.generate_cases(num_cases_per_category)
            test_cases.extend(cases)
        return test_cases

class TestCase:
    def __init__(self, code, question, expected_insights, difficulty):
        self.code = code
        self.question = question
        self.expected_insights = expected_insights
        self.difficulty = difficulty
        self.ground_truth = self._establish_ground_truth()
    
    def _establish_ground_truth(self):
        """Manually establish the correct answer for evaluation."""
        pass
```

### Representation Converter

```python
class RepresentationConverter:
    def __init__(self):
        self.holoform_generator = HoloformGenerator()
        self.ast_generator = ASTGenerator()
    
    def convert_to_representations(self, test_case):
        """Convert test case code to all representation formats."""
        return {
            'raw': test_case.code,
            'holoform': self._to_holoform_text(test_case.code),
            'ast': self._to_ast_text(test_case.code)
        }
    
    def _to_holoform_text(self, code):
        """Convert code to human-readable Holoform representation."""
        holoforms = self.holoform_generator.generate_from_code(code)
        return self._serialize_holoforms(holoforms)
    
    def _to_ast_text(self, code):
        """Convert code to human-readable AST representation."""
        ast_tree = ast.parse(code)
        return ast.dump(ast_tree, indent=2)
```

### LLM Evaluator

```python
class LLMEvaluator:
    def __init__(self, llm_client):
        self.llm_client = llm_client
        self.prompt_templates = {
            'raw': "Analyze this Python code and answer the question:\n\nCode:\n{code}\n\nQuestion: {question}",
            'holoform': "Analyze this Holoform representation and answer the question:\n\nHoloform:\n{representation}\n\nQuestion: {question}",
            'ast': "Analyze this AST representation and answer the question:\n\nAST:\n{representation}\n\nQuestion: {question}"
        }
    
    def evaluate_test_case(self, test_case, representations):
        """Evaluate a test case across all representations."""
        results = {}
        for rep_type, representation in representations.items():
            prompt = self.prompt_templates[rep_type].format(
                code=representation if rep_type == 'raw' else '',
                representation=representation if rep_type != 'raw' else '',
                question=test_case.question
            )
            response = self.llm_client.generate(prompt)
            results[rep_type] = response
        return results
```

### Response Analyzer

```python
class ResponseAnalyzer:
    def __init__(self):
        self.scoring_criteria = {
            'accuracy': self._score_accuracy,
            'completeness': self._score_completeness,
            'insight_depth': self._score_insight_depth
        }
    
    def analyze_responses(self, test_case, llm_responses):
        """Analyze and score LLM responses for a test case."""
        scores = {}
        for rep_type, response in llm_responses.items():
            scores[rep_type] = self._score_response(test_case, response)
        return scores
    
    def _score_response(self, test_case, response):
        """Score a single response across all criteria."""
        scores = {}
        for criterion, scorer in self.scoring_criteria.items():
            scores[criterion] = scorer(test_case, response)
        return scores
    
    def _score_accuracy(self, test_case, response):
        """Score how accurately the response answers the question."""
        # Compare against ground truth
        # Return score 0-1
        pass
    
    def _score_completeness(self, test_case, response):
        """Score how completely the response addresses all aspects."""
        # Check if all expected insights are covered
        # Return score 0-1
        pass
    
    def _score_insight_depth(self, test_case, response):
        """Score the depth of understanding demonstrated."""
        # Evaluate explanation quality and reasoning
        # Return score 0-1
        pass
```

## Data Models

### Experiment Results

```python
class ExperimentResult:
    def __init__(self):
        self.test_cases = []
        self.representation_scores = {
            'raw': {'accuracy': [], 'completeness': [], 'insight_depth': []},
            'holoform': {'accuracy': [], 'completeness': [], 'insight_depth': []},
            'ast': {'accuracy': [], 'completeness': [], 'insight_depth': []}
        }
        self.magic_moments = []  # Cases where Holoform significantly outperformed
    
    def add_test_result(self, test_case, scores):
        """Add results from a single test case."""
        self.test_cases.append(test_case)
        for rep_type, rep_scores in scores.items():
            for criterion, score in rep_scores.items():
                self.representation_scores[rep_type][criterion].append(score)
    
    def identify_magic_moments(self, threshold=0.2):
        """Identify cases where Holoform significantly outperformed others."""
        magic_moments = []
        for i, test_case in enumerate(self.test_cases):
            holoform_avg = self._get_average_score('holoform', i)
            raw_avg = self._get_average_score('raw', i)
            ast_avg = self._get_average_score('ast', i)
            
            if holoform_avg > raw_avg + threshold and holoform_avg > ast_avg + threshold:
                magic_moments.append({
                    'test_case': test_case,
                    'holoform_score': holoform_avg,
                    'raw_score': raw_avg,
                    'ast_score': ast_avg,
                    'improvement': holoform_avg - max(raw_avg, ast_avg)
                })
        
        return magic_moments
```

## Testing Strategy

### Experiment Execution

1. **Generate Test Cases**: Create 15 test cases across the three categories
2. **Convert Representations**: Transform each test case into raw, Holoform, and AST formats
3. **LLM Evaluation**: Present each representation to the LLM with the test question
4. **Response Analysis**: Score responses objectively across accuracy, completeness, and insight depth
5. **Magic Moment Identification**: Find cases where Holoforms significantly outperformed other representations

### Success Criteria

The experiment will be considered successful if:
- Holoforms demonstrate superior performance in at least 30% of test cases
- At least 3 "magic moments" are identified where Holoforms provide significantly better insights
- Specific categories of problems are identified where Holoforms excel

### Expected Outcomes

We expect to find that Holoforms excel in:
- **Cross-function data flow analysis**: Where understanding requires tracing data through multiple function calls
- **State modification tracking**: Where side effects and state changes are abstracted clearly
- **Call graph reasoning**: Where understanding dependencies between code components is crucial

## Implementation Plan

1. **Create Test Cases** (2-3 days)
   - Develop 5 examples for each category
   - Establish ground truth answers
   - Validate test case quality

2. **Build Experiment Framework** (3-4 days)
   - Implement representation converter
   - Create LLM evaluator
   - Build response analyzer

3. **Run Experiment** (1-2 days)
   - Execute all test cases
   - Collect LLM responses
   - Score and analyze results

4. **Analyze Results** (1-2 days)
   - Identify magic moments
   - Document specific insights
   - Prepare findings report

This focused experiment should reveal whether Holoforms truly provide that "nugget of promise" you're looking for - concrete evidence that this approach offers unique value for AI code understanding.