# NEVER SIMULATE AI INVOLVEMENT

## Critical Project Rule

**WE NEVER EVER SIMULATE THE INVOLVEMENT OF AN AI.**

This is not possible. It's fake. It's misleading. It's wrong.

## What This Means

### ❌ NEVER DO THIS:
- Mock LLM responses with pattern matching
- Fake AI evaluation results
- Simulate "AI understanding" with if/else logic
- Pretend to measure AI performance without real AI
- Create fake benchmarks that look like AI testing

### ✅ ALWAYS DO THIS:
- Use real LLM APIs (OpenAI, Anthropic, etc.)
- Test with actual local models (Ollama, etc.)
- Manual testing with real AI assistants
- Honest placeholders that clearly state "NOT TESTED WITH REAL AI"
- Real measurements with real AI responses

## Why This Rule Exists

1. **AI behavior is unpredictable** - You cannot simulate it
2. **Pattern matching ≠ AI reasoning** - Completely different
3. **Fake results are worse than no results** - They mislead
4. **Real validation is the only validation** - Everything else is theater

## Current Project Status

The MockLLM in `eval.py` is **FAKE** and produces **MEANINGLESS RESULTS**.

The "22.22% accuracy improvement" is **NOT REAL** - it's just programmed pattern matching.

## How to Fix This

### Option 1: Real API Integration
```python
import openai
# Actually call GPT-3.5/4 with real prompts
```

### Option 2: Local Model Testing  
```python
import ollama
# Actually run Llama2/CodeLlama locally
```

### Option 3: Manual Testing
```python
# Generate prompts, save to files
# Human feeds to real AI
# Record actual responses
```

### Option 4: Honest Placeholder
```python
class PlaceholderLLM:
    def query(self, prompt: str) -> str:
        return "NOT_TESTED_WITH_REAL_AI - Replace this with actual LLM"
```

## Remember

**If you're not calling a real AI, you're not testing AI performance.**

**Period.**

---

*This rule exists because simulating AI is impossible and leads to false conclusions about what actually works.*