# Validation Criteria for Codon Testing

**Date:** July 18, 2025  
**Phase:** Codon Refinement and Validation  
**Purpose:** Ensure consistent, objective evaluation of AI comprehension

## Scoring Framework

### Pass/Fail Thresholds
- **PASS (100%):** All criteria met perfectly
- **STRONG PASS (80-99%):** 80%+ criteria met with minor gaps
- **WEAK PASS (60-79%):** 60-79% criteria met with notable gaps
- **FAIL (<60%):** Less than 60% criteria met

### Success Targets by Difficulty
- **Basic:** 90%+ pass rate (PASS or STRONG PASS)
- **Intermediate:** 80%+ pass rate (PASS or STRONG PASS)
- **Advanced:** 70%+ pass rate (PASS or STRONG PASS)
- **Expert:** 60%+ pass rate (PASS or STRONG PASS)

## Evaluation Guidelines

### What Counts as "Meeting Criteria"

#### 1. Pattern Recognition
**PASS:** AI correctly identifies the computational category (flow, condition, assignment, context)
**FAIL:** AI misidentifies the category or shows no understanding

#### 2. Semantic Understanding
**PASS:** AI demonstrates understanding of what the pattern does behaviorally
**PARTIAL:** AI shows partial understanding but misses key aspects
**FAIL:** AI shows no understanding of the pattern's behavior

#### 3. Execution Sequence
**PASS:** AI correctly describes the order of operations
**PARTIAL:** AI describes most of the sequence correctly
**FAIL:** AI cannot describe the execution order or gets it wrong

#### 4. Context Awareness
**PASS:** AI doesn't ask for additional context when instructed not to
**FAIL:** AI requests original code or additional context despite instructions

#### 5. Error Handling (Intermediate+)
**PASS:** AI addresses error handling appropriately (either describes it or notes its absence)
**PARTIAL:** AI mentions errors but doesn't fully address handling
**FAIL:** AI ignores error handling entirely

### Keyword Recognition

#### Core Keywords by Pattern Type
- **Flow patterns (>):** pipeline, sequential, flow, execution, process
- **Condition patterns (?):** conditional, if, test, guard, check
- **Assignment patterns (=):** assign, set, bind, result, value
- **Context patterns (@):** scope, context, within, environment, resource

#### Advanced Keywords
- **Error handling:** error, exception, failure, recovery, fallback
- **Resource management:** cleanup, resource, lifecycle, acquire, release
- **Concurrency:** thread, concurrent, race, synchronization, lock

## Common Evaluation Pitfalls

### What NOT to Penalize
1. **Different terminology:** If AI says "sequential processing" instead of "pipeline" - still counts
2. **Additional insights:** If AI provides extra relevant information - bonus points
3. **Cautious language:** If AI says "appears to" or "seems to" - still counts if correct

### What TO Penalize
1. **Requesting context:** When explicitly told not to ask for more information
2. **Wrong category:** Calling a flow pattern a condition pattern, etc.
3. **Backwards execution:** Getting the order of operations wrong
4. **Ignoring symbols:** Not using the provided symbol meanings
5. **Symbol confusion:** Mixing up what >, =, ?, @ represent despite being told

## Detailed Scoring Examples

### Example 1: Strong Response
**AI Response:** "This pattern represents a sequential pipeline that assigns the final result. The > symbols indicate flow from one operation to the next, and the = indicates assignment of the final value."

**Scoring:**
- Pattern Recognition: ✅ PASS (correctly identifies flow/assignment)
- Semantic Understanding: ✅ PASS (understands pipeline behavior)
- Execution Sequence: ✅ PASS (describes sequential flow)
- Context Awareness: ✅ PASS (doesn't ask for more info)

**Result:** 4/4 = 100% = PASS

### Example 2: Partial Response
**AI Response:** "This looks like some kind of assignment operation, but I'd need to see the original code to understand what's being assigned."

**Scoring:**
- Pattern Recognition: ⚠️ PARTIAL (recognizes assignment but misses flow)
- Semantic Understanding: ❌ FAIL (doesn't understand pipeline)
- Execution Sequence: ❌ FAIL (no sequence described)
- Context Awareness: ❌ FAIL (asks for original code)

**Result:** 0.5/4 = 12.5% = FAIL

### Example 3: Good but Incomplete
**AI Response:** "This represents a pipeline operation where data flows through multiple stages. The final result is assigned to a variable."

**Scoring:**
- Pattern Recognition: ✅ PASS (correctly identifies flow/assignment)
- Semantic Understanding: ✅ PASS (understands pipeline)
- Execution Sequence: ⚠️ PARTIAL (mentions stages but not detailed sequence)
- Context Awareness: ✅ PASS (doesn't ask for more info)

**Result:** 3.5/4 = 87.5% = STRONG PASS

## Quality Indicators

### Excellent Response Indicators
- Uses precise technical language
- Describes execution order clearly
- Recognizes symbol meanings
- Provides relevant examples or analogies
- Addresses error handling appropriately

### Poor Response Indicators
- Vague or generic language
- Requests additional context
- Misidentifies pattern category
- Gets execution order wrong
- Ignores symbol meanings entirely

## Documentation Requirements

### For Each Test Record:
1. **Full AI Response:** Copy exact response
2. **Criterion-by-Criterion Scoring:** Check each criterion individually
3. **Keyword Analysis:** Note which expected keywords appeared
4. **Overall Assessment:** PASS/STRONG PASS/WEAK PASS/FAIL
5. **Notes:** Any interesting observations or patterns

### Summary Statistics to Track:
- Pass rates by difficulty level
- Pass rates by AI model
- Most/least understood patterns
- Common failure modes
- Keyword recognition rates

---

**Validation Status:** Framework Complete  
**Next Step:** Begin systematic testing with TEST-001