# HoloChain Symbol Vocabulary v0

*A minimal, token-efficient symbolic language for representing code behavior, causal chains, and queryable semantics in the Holoform research project.*

---

## 0. Why This Exists

LLMs burn vast tokens when forced to ingest raw source for simple reasoning (e.g., state mutation across two small functions). **HoloChain** notation gives us a *compressed, loss-aware* layer that captures *just the decisive semantics* needed to answer many program-understanding questions. It is:

* **Compact** — optimized for token cost across common BPEs.
* **Composable** — chains can be concatenated, referenced, merged.
* **Machine-parseable** — regular-enough grammar for round‑trip tooling.
* **Human legible** — glyph or ASCII modes.
* **Loss-graded** — deliberately discards trivia; preserves effects & guards.

This doc specifies **v0**: a core vocabulary + grammar sufficient to encode the “magic moment” example (login\_count, analyze\_data, discount) *and* generalize to \~80% of everyday code-understanding asks.

---

## 1. Design Principles

| Principle                 | Why                                  | Implication                                                              |
| ------------------------- | ------------------------------------ | ------------------------------------------------------------------------ |
| **Token Predictability**  | Lower cost; stable across models     | Prefer ASCII digraphs (->, :=, &&) in compression mode; glyphs optional. |
| **Semantic Minimalism**   | Only what’s needed for reasoning     | Encode guards, assignments, returns, side-effects; omit formatting.      |
| **Causal Directionality** | Many questions are "if X then what?" | Use left→right causal flow; guard precedes effect.                       |
| **Referencable Units**    | Programmatic tooling                 | Every chain has an **ID** & optional provenance (file\:line).            |
| **Progressive Fidelity**  | Ladder to raw code                   | Can expand ID → Holoform → Source when needed.                           |

---

## 2. Encoding Modes

HoloChain supports two parallel surface syntaxes.

### 2.1 Glyph Mode (GM)

Readable; visually compact when rendered; good for docs & humans.

* Arrow: `→`
* Assign: `:=`
* And/Or/Not: `&`, `|`, `!`
* Conditional: `?` *...then...* `:` *else...*
* Selection/Appends: `⇐` (read “selected into / appended to”)

### 2.2 ASCII Compression Mode (ACM)

Strict 7‑bit ASCII; tuned for tokenizer merges.

* Arrow: `->`
* Assign: `=` **(default)** or `:=` (strict); choose model-calibrated cheapest token.
* And/Or/Not: `&&`, `||`, `!`
* Conditional: `? :`
* Selection/Appends: `<=` (maps to `⇐`)

> **Rule:** A HoloChain emitter may output both GM & ACM; downstream prompters pick ACM for cost‑critical LLM calls.

---

## 3. Lexical Elements

**Identifiers**
`ID` = `[A-Za-z_][A-Za-z0-9_./-]*` (paths allowed; keep short).
Use canonical short names: `login`, `status`, `prio`, `cust1`, `yrs`.

**Literals**
Numbers: `123`, `0.15`, `-2`
Strings (short): `'x'` or `"x"`; long strings hashed.

**Predicates**
Comparison ops: `==`, `!=`, `>`, `>=`, `<`, `<=`.

**Group**
Parentheses `(` `)` for precedence.

**Line Terminator**
Newline ends a chain statement.

---

## 4. Core Production Types

We define 5 top-level symbolic record types. Each line starts with a 1‑char tag + `:`.

| Tag  | Type                                     | Purpose                  | Example                             |   |                            |
| ---- | ---------------------------------------- | ------------------------ | ----------------------------------- | - | -------------------------- |
| `F:` | Function signature/meta                  | name(args)->rets         | `F:process_user_data(u)`            |   |                            |
| `G:` | Guarded effect chain                     | cond -> effect -> effect | `G:!email->status=invalid->login=0` |   |                            |
| `S:` | Selection rule (collection add / filter) | expr <= target           | \`S:(crit&\&prio>8)                 |   | (norm&\&prio>5)<=results\` |
| `C:` | Constant/enum mapping                    | sym=value                | `C:gold_rate=0.15`                  |   |                            |
| `R:` | Return/value derivation                  | expr -> out              | `R:total*(1-rate)->pay`             |   |                            |

All tags accept optional provenance suffix: `#file@L42`.

---

## 5. Minimal Grammar (EBNF-ish)

```
record        = func | guard_chain | select_rule | const_def | ret_rule ;
func          = 'F:' ident '(' [param_list] ')' [ret_clause] [prov] ;
param_list    = ident {',' ident} ;
ret_clause    = '->' ident {',' ident} ;
prov          = '#' file '@' line ;

guard_chain   = 'G:' cond '->' effect { '->' effect } [prov] ;
select_rule   = 'S:' cond '<=' ident [prov] ;
const_def     = 'C:' ident '=' literal [prov] ;
ret_rule      = 'R:' expr '->' ident [prov] ;

cond          = disj ;
disj          = conj { '||' conj } ;
conj          = neg { '&&' neg } ;
neg           = [ '!' ] atom ;
atom          = comparison | '(' cond ')' ;
comparison    = ident cmpop literal | ident cmpop ident ;
cmpop         = '==','!=','>','>=','<','<=' ;

effect        = assign | call | annotate ;
assign        = ident '=' expr ;
call          = ident '(' [arg_list] ')' ;
annotate      = '+' ident | '-' ident  (* e.g., mark processed / skipped *) ;

expr          = term { ('+'|'-'|'*'|'/') term } ;
term          = factor ;  (* intentionally shallow for v0 *)
factor        = literal | ident | '(' expr ')' ;
```

---

## 6. Semantics Cheatsheet

| Syntax    | Meaning                                                                       | Notes                                             |                     |               |
| --------- | ----------------------------------------------------------------------------- | ------------------------------------------------- | ------------------- | ------------- |
| `A->B`    | When A holds (state/event), B eventually executed/applied.                    | Sequential causal flow.                           |                     |               |
| `cond<=X` | Items satisfying `cond` are **added to** or **selected into** collection `X`. | For append/filter ops.                            |                     |               |
| `x=y`     | Assign / mutate.                                                              | Use canonical short var names.                    |                     |               |
| `!A`      | Not A.                                                                        | Use sparingly; expand if ambiguous.               |                     |               |
| `A&&B`    | A and B both true.                                                            | Short-circuit semantics implied.                  |                     |               |
| \`A       |                                                                               | B\`                                               | Either A or B true. | Inclusive or. |
| `A?B:C`   | If A then B else C.                                                           | Nested supported but costly; flatten if possible. |                     |               |

---

## 7. Mapping Common Code Patterns → HoloChain

### 7.1 Chained State Change (Magic Moment)

Python:

```py
if not user.email:
    user.status = "invalid"
    user.login_count = 0
```

HoloChain (GM):

```
G:!email→status:=invalid→login:=0#user.py@L10
```

HoloChain (ACM):

```
G:!email->status=invalid->login=0#user.py@L10
```

### 7.2 Selection Rule w/ Multi-Branch Collapse

Original logic:

```py
if item.type == 'critical' and item.priority > 8:
    results.append(item)
elif item.type == 'normal' and item.priority > 5:
    results.append(transform(item))
```

HoloChain:

```
S:(type==critical&&prio>8)||(type==normal&&prio>5)<=results#data.py@L30
```

*Transformation side-effect optional; encode separately if meaningfully changes item.*

### 7.3 Tiered Discount

```py
if tier=="gold" and yrs>=3: rate=.15
elif tier=="silver" and yrs>=2: rate=.10
else: rate=.05
pay=total*(1-rate)
```

HoloChain:

```
G:tier==gold&&yrs>=3->rate=.15
g:tier==silver&&yrs>=2->rate=.10
g:else->rate=.05
R:total*(1-rate)->pay
```

> Lowercase `g:` lines permitted for secondary/ordered guards inside same fn scope; parser folds them into a decision table.

---

## 8. Scope & Namespacing

**Fully Qualified Symbol**: `pkg/mod/file::fn.var` is most robust but token-heavy. v0 recommends *Context Header* providing ambient scope so inline chains can use short symbols.

**Context Header Example**

```
CTX:user_module user=status,login,email
CTX:order_module cust=tier,yrs rate,total,pay
```

Prompters send CTX once, then short names in records; LLM cost drops drastically.

---

## 9. Provenance & Round‑Trip

Each record can carry provenance so tooling can re-expand to source.

**Format:** `#<relpath>@L<start>[-L<end>]`

* Optional; omit in extreme compression.
* Range allowed for multi-line spans.
* Hash extension allowed: `#user.py@L10^a1b2c3`.

---

## 10. Compression Heuristics

| Technique                                          | Savings | Risk             | When                             |
| -------------------------------------------------- | ------- | ---------------- | -------------------------------- |
| Drop keywords (`if`, `elif`, `return`)             | High    | Low              | Always; structural in grammar.   |
| Short var aliases (login→l)                        | High    | Med              | Only under CTX mapping.          |
| Collapse multi-branch into single `S:` disjunction | Med     | Med              | When shared effect (append).     |
| Strip provenance                                   | Med     | Tool loses trace | Only for pure reasoning queries. |
| Numeric tier tables → `C:` constants               | Low     | Low              | Good for repeated values.        |

---

## 11. Formatting Conventions for Prompts

**Problem Card Template (ACM)**

```
#HoloChain v0
F:process_user_data(u)
G:!email->status=invalid->login=0
S:(type==critical&&prio>8)||(type==normal&&prio>5)<=results
G:tier==gold&&yrs>=3->rate=.15
g:tier==silver&&yrs>=2->rate=.10
g:else->rate=.05
R:total*(1-rate)->pay

TASK:Answer fully:1 login?2 add conds?3 pay for cust1(total=100,tier=gold,yrs=5)
FORMAT:bullet lines;include $ amt.
```

**Expected Model Output (Human-Friendly)**

```
login_count is set to 0.
If: type=="critical" & prio>8 OR type=="normal" & prio>5.
$85.00 (15% off $100).
```

---

## 12. Evaluation Hooks

To benchmark:

1. Emit Problem Cards from N code snippets.
2. Query LLM with ACM vs GM vs Raw source.
3. Score structured answers.
4. Track tokens + \$ from provider ledger (hook exists in BRAIN).
5. Compare accuracy deltas vs. compression ratio.

---

## 13. Open Questions for v1

* Represent loops compactly? (`∀x∈items:cond(x)<=results`?)
* Encode side-effectful transforms vs. pure selection?
* Model mutation order vs. eventual state? (Temporal granularity.)
* Represent uncertain / union states cheaply (`status∈{active,invalid}`)?
* Auto-aliasing dictionaries / attrs (user.status→status)?

---

## 14. Next Steps

**Pick one to continue:**

1. Build toy parser (Python) that emits v0 ACM chains from small modules.
2. Generate 50 Problem Cards from sample corpus; measure token vs. accuracy.
3. Integrate Context Header emission into existing BRAIN embed/search CLI.
4. Define reserved short aliases (status→st, login→lg, priority→p) & test token impact.

---

**Ready to dive into implementation? Tell me which next step to tackle and we’ll scaffold code.**
