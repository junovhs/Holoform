# Holoform - Weekend Hacker Edition

> "One-skilled-hacker-on-weekends" proof of concept for computational DNA compression

## What This Is

A minimal demo framework for testing whether "Holoforms" (structured AST representations) can make LLMs understand code better while using fewer tokens.

**⚠️ IMPORTANT**: Current evaluation uses fake MockLLM. See `NEVER_SIMULATE_AI.md` for real testing requirements.

## Quick Start

```bash
# Install deps
pip install -r requirements.txt

# Run the demo
bash run.sh
```

## The 5-Weekend Plan

- **W-0** ✅ Starter kit (you are here)
- **W-1** ⏳ Holoform generator (`holoform.py`)
- **W-2** ⏳ Tiny evaluator (`eval.py`) 
- **W-3** ⏳ Compression experiment (`symbolic_chain.py`)
- **W-4** ⏳ Real-world smoke test
- **W-5** ⏳ Screencast & write-up

## Success Metric

Does Holoform make the LLM pick the right answer more often on 5 toy tasks? **Yes = project success.**

## Files

- `holoform.py` - AST → JSON converter (≤250 LoC)
- `eval.py` - LLM evaluation harness (≤150 LoC)  
- `symbolic_chain.py` - Token compressor (≤100 LoC)
- `examples/` - Test cases
- `results.md` - Metrics table
- `demo.webm` - Screen recording

---

*Keep it scrappy. Ship it.*