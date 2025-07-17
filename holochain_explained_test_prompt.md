# HoloChain Test Prompt with Explanation

## Copy and paste this complete prompt to an AI:

---

**HOLOCHAIN NOTATION EXPLANATION:**

HoloChain is a symbolic notation that represents code behavior using these symbols:

- `F:` = Function definition: `F:function_name(params)->output`
- `G:` = Guarded effect chain: `G:condition->effect->effect->result`
- `R:` = Return value: `R:value`
- `->` = Causal flow (then/causes)
- `!` = NOT (logical negation)
- `&&` = AND (logical and)
- `||` = OR (logical or)
- `==` = Equals comparison

**Example:**
```python
if not user.active:
    user.status = "inactive"
    return "disabled"
```
Becomes: `G:!active->status=inactive->R:disabled`

**Reading Guide:**
- `G:!email->status=invalid->login_count=0->R:email_required` means:
  "IF email is missing, THEN set status to invalid, THEN set login_count to 0, THEN return 'email_required'"

---

**NOW ANALYZE THIS HOLOCHAIN:**

```
F:process_user_login(user)->result
G:!email->status=invalid->login_count=0->R:email_required
G:status==banned->login_count=0->R:account_banned
G:failed_attempts>5->status=locked->login_count=0->R:account_locked
G:else->login_count=login_count+1->R:login_successful
```

**Question:** List ALL the conditions under which login_count gets set to 0.

Please provide a precise, step-by-step answer.

---