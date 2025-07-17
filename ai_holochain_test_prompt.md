# HoloChain Creation Test Prompt

## Background
HoloChain is a **language-agnostic** symbolic notation system that captures universal computational patterns. Think of it as distilling code down to fundamental semantic behaviors that would be recognizable even to aliens - focusing on **causal relationships** and **behavioral patterns** that exist across all programming languages, not syntax-specific details.

The goal is to create representations so fundamental that the same HoloChain notation could represent equivalent logic whether written in Python, Rust, JavaScript, C++, or any other language.

## HoloChain Symbolic Vocabulary

### Core Production Types:
- `F:` - Function signature: `F:function_name(params)->output`
- `G:` - Guarded effect chain: `G:condition->effect->effect`
- `S:` - Selection rule: `S:condition<=target::transformation`
- `C:` - Constant/enum: `C:name=value`
- `R:` - Return/derivation: `R:expression->output`
- `CTX:` - Context header: `CTX:scope var1=type1,var2=type2`

### Symbolic Operators:
- `->` - Causal flow (then)
- `<=` - Selection into (append/filter)
- `::` - Transformation
- `&&` - Logical AND
- `||` - Logical OR
- `!` - Logical NOT
- `∈` - Element of (in)
- `∉` - Not element of (not in)
- `++` - Increment
- `==` - Equals

### Key Principles:
1. **Causal chains**: Show cause-effect relationships directly
2. **Pattern abstraction**: Focus on semantic behavior, not syntax
3. **Context efficiency**: Use context headers to define variable mappings once
4. **Token optimization**: Eliminate syntactic noise, preserve semantic meaning

## Examples:

### State Modification Pattern:
```python
if not user.email:
    user.status = "invalid"
    user.login_count = 0
```
**HoloChain:** `G:!email->status=invalid->login=0`

### Selection Pattern:
```python
results = []
for item in items:
    if item.priority > 5:
        results.append(item.transform())
```
**HoloChain:** `S:priority>5<=results::transform()`

### Complex Conditional:
```python
if user.type == "premium" and user.years > 3:
    rate = 0.15
elif user.type == "regular":
    rate = 0.10
else:
    rate = 0.05
```
**HoloChain:** 
```
G:type==premium&&years>3->rate=0.15
G:type==regular->rate=0.10
G:else->rate=0.05
```

## Your Task:
Given the following Python code, create a HoloChain representation that:
1. Captures the essential semantic behavior
2. Uses appropriate symbolic notation
3. Minimizes token count while preserving meaning
4. Follows the causal flow principle (condition->effect)

**Please provide:**
1. The HoloChain representation
2. Brief explanation of your approach
3. Any context headers you used

---

**Code to convert:**
[USER WILL INSERT CODE HERE]

---

**Expected format:**
```
CTX: [context headers if needed]

[HoloChain representation using F:, G:, S:, R:, C: notation]
```

**Explanation:** [Brief explanation of your approach and any design decisions]