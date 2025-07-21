# Holoform Project Guide

## For AI Assistants Working on This Project

This guide helps AI assistants understand the Holoform project structure and contribute effectively.

## Project Overview

**Holoform** is a "computational DNA" system that converts Python code into structured JSON representations (Holoforms) to improve LLM code understanding while reducing token usage.

### Core Concept
- **Input**: Python source code
- **Process**: AST → Structured JSON (Holoform) → Optional compression
- **Output**: Better LLM understanding with fewer tokens

## Architecture

### Core Files (Weekend Hacker Edition)

1. **`holoform.py`** (≤250 LoC) - AST to JSON converter
   - Parses Python AST using `ast` module
   - Extracts functions, classes, complexity, dependencies
   - Outputs structured JSON representations

2. **`eval.py`** (≤150 LoC) - LLM evaluation harness
   - Compares raw code vs Holoform performance
   - Uses mock LLM for demonstration (replace with real LLM)
   - Measures accuracy improvements

3. **`symbolic_chain.py`** (≤100 LoC) - Token compressor
   - Replaces repeated strings with symbols (§1, §2, etc.)
   - Calculates compression ratios
   - Includes decompression capability

### Supporting Files

- **`examples/sample.py`** - Test cases (fibonacci, Calculator class, process_numbers)
- **`run.ps1`** / **`run.sh`** - Demo runners
- **`requirements.txt`** - Dependencies (tiktoken, openai)
- **`TODO-ICEBOX.md`** - Scope management

## Key Data Structures

### Holoform JSON Schema
```json
{
  "type": "function|class",
  "name": "function_name",
  "scope": "parent.scope",
  "signature": {
    "args": ["arg1", "arg2"],
    "defaults": 0,
    "returns": "return_type"
  },
  "body_structure": {
    "statements": 3,
    "control_flow": ["if", "for"],
    "operations": ["assign", "return"],
    "calls": ["func_name"]
  },
  "complexity": 2,
  "dependencies": ["var1", "func2"],
  "docstring": "Function description"
}
```

## Success Metrics

**Primary Goal**: Does Holoform make LLM pick the right answer more often on 5 toy tasks?

**IMPORTANT**: Current MockLLM results are **FAKE** and meaningless. See `NEVER_SIMULATE_AI.md`.

Real testing requires:
- Actual LLM API calls (OpenAI, Anthropic, etc.)
- Local model testing (Ollama, etc.)  
- Manual evaluation with real AI assistants

## Development Guidelines

### For AI Assistants

1. **Stay Minimal**: Weekend hacker approach - only essential features
2. **Single Success Metric**: Focus on LLM accuracy improvement
3. **Use TODO-ICEBOX.md**: Log feature ideas but don't implement them
4. **Test-Driven**: Always test changes with `run.ps1`

### Code Style
- Python 3.8+ compatible
- Type hints where helpful
- Docstrings for public functions
- Error handling for file operations

### Testing Workflow
```bash
# Generate Holoforms
python holoform.py examples/sample.py > holoforms.json

# Run evaluation
python eval.py examples/sample.py holoforms.json

# Test compression
python symbolic_chain.py holoforms.json

# Full demo
powershell -ExecutionPolicy Bypass -File run.ps1
```

## Extension Points

### Easy Wins
1. **Real LLM Integration**: Replace MockLLM with OpenAI/local model
2. **More Test Cases**: Add examples in `examples/`
3. **Better Compression**: Improve symbolic_chain algorithm
4. **Token Counting**: Use tiktoken for accurate counts

### Advanced Features (Icebox)
- Multi-language support
- Web UI
- Database storage
- Performance optimizations
- CI/CD pipeline

## File Generation Patterns

When creating new test files:
```python
# examples/new_test.py
def example_function(param):
    """Clear docstring for LLM testing"""
    # Simple logic for evaluation
    return result

class ExampleClass:
    def __init__(self):
        self.attribute = value
    
    def method(self):
        return self.attribute
```

## Common Tasks

### Adding New Holoform Fields
1. Modify `HoloformGenerator.visit_FunctionDef()` or `visit_ClassDef()`
2. Add extraction logic in helper methods
3. Test with existing examples
4. Update schema documentation

### Improving Compression
1. Modify `SymbolicChainCompressor.compress()`
2. Adjust frequency thresholds
3. Test compression ratios
4. Ensure decompression works

### Better Evaluation
1. Enhance `MockLLM` or integrate real LLM
2. Add more test cases in `HoloformEvaluator.test_cases`
3. Improve accuracy calculation
4. Add timing metrics

## Debugging Tips

### Common Issues
- **JSON encoding**: Use UTF-8, avoid BOM
- **AST parsing**: Handle syntax errors gracefully  
- **File paths**: Use relative paths from project root
- **Windows compatibility**: Test PowerShell scripts

### Validation Commands
```bash
# Validate JSON output
python -c "import json; print('Valid:', bool(json.load(open('holoforms.json'))))"

# Check file encoding
python -c "with open('holoforms.json', 'rb') as f: print(f.read()[:20])"

# Test AST parsing
python -c "import ast; ast.parse(open('examples/sample.py').read())"
```

## Project Philosophy

**"One-skilled-hacker-on-weekends"** approach:
- Single-threaded development
- Python only
- No fancy infrastructure
- Progress = working demo
- Ship scrappy, iterate later

Remember: If it doesn't directly improve the LLM accuracy metric, it goes in the icebox! 🧊