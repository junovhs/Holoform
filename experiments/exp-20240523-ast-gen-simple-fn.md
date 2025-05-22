# Experiment Report: AST-Based Holoform Generation for Simple Functions (v1)

**Date:** YYYY-MM-DD *(Please replace YYYY-MM-DD with today's date)*
**Branch:** `task/auto-gen-v1`
**Associated Commits (Latest):** `5369a68` *(This is the hash of your last "Fix" commit. We'll update if more are made for this phase)*

## 1. Overview

**Purpose:** To validate the feasibility of automatically generating basic Holoform data structures from Python source code using Abstract Syntax Tree (AST) parsing. This experiment focuses on simple, self-contained functions with no internal calls to other user-defined functions.

**Hypothesis:** Python's `ast` module can be used to extract key features of a function (name, parameters, simple operations, return values, docstrings, comments) and map them into a predefined Holoform dictionary structure with reasonable accuracy for description and operational representation.

## 2. Configuration

-   **Target Language:** Python
-   **Core Tool:** Python `ast` module, `json` module.
-   **Input:** Python functions as multi-line strings (`G_helper_gt_correct_docstring`, `G_helper_gt_correct_comment`, `G_helper_gt_correct_no_desc`).
-   **Output:** JSON-like Holoform dictionary structure.
-   **Key Script:** `src/holoform_generators/ast_basic_generator.py`

## 3. Process

1.  Defined multiple Python function strings with varying documentation styles (docstring, preceding comment block, no explicit description).
2.  Developed a `HoloformGeneratorVisitor` class (subclass of `ast.NodeVisitor`) to traverse the AST of a parsed function.
3.  Implemented visitor methods (`visit_FunctionDef`, `visit_Assign`, `visit_Return`) to extract:
    *   Function ID (from name).
    *   Input parameters.
    *   Description (prioritizing docstring, then comment block above function, then a generated default).
    *   Operations (assignments, with `semantic_purpose` derived from inline comments or default, and `expression_ast_repr` capturing the RHS structure).
    *   Output variable name (from return statement).
4.  Added logic to normalize whitespace and comment markers in descriptions for consistent output.
5.  Ran test scenarios comparing generated Holoforms against manually defined "expected" Holoform structures, focusing on description accuracy and core operational details.

## 4. Results & Metrics

| Test Scenario                     | Description Extraction                                 | Op AST Repr. | Op Semantic Purpose | Params | Output Var | Overall Scenario Result |
| :-------------------------------- | :----------------------------------------------------- | :----------- | :------------------ | :----- | :--------- | :---------------------- |
| `with_docstring`                  | ✅ SUCCESS (Multiline docstring correctly extracted)     | ✅ SUCCESS   | ✅ SUCCESS          | ✅     | ✅         | ✅ PASS                 |
| `with_comment_only`               | ✅ SUCCESS (Multiline comment block correctly extracted) | ✅ SUCCESS   | ✅ SUCCESS          | ✅     | ✅         | ✅ PASS                 |
| `no_desc_defined`                 | ✅ SUCCESS (Sensible default generated)                | ✅ SUCCESS   | ✅ SUCCESS          | ✅     | ✅         | ✅ PASS                 |

**Key Quantitative Results:**
-   All three test scenarios for description extraction passed successfully.
-   Core operational details (parameter names, AST structure of assignment RHS, output variable name, inline comment for semantic purpose) were correctly captured.

**Qualitative Results:**
-   The `expression_ast_repr` (e.g., `"BinOp(BinOp(Name(id='val1'), Mult, Constant(value_type='number')), Add, Name(id='val2'))"`) provides a good, language-agnostic (within Python AST terms) representation of the expression's structure without being tied to specific literal values.
-   Extraction of inline comments for `semantic_purpose` of operations adds valuable developer intent to the Holoform.

## 5. Analysis & Discussion

This initial version of the AST-based Holoform generator demonstrates strong potential. It can successfully parse simple Python functions and produce structured Holoforms that accurately reflect the function's interface, core operations, and descriptive information derived from common documentation practices (docstrings, comments).

**Successes:**
-   Robust handling of different description sources.
-   Accurate extraction of function signature elements.
-   Correct structural representation of simple arithmetic expressions.
-   Incorporation of developer intent through inline comment parsing for operations.

**Limitations & Next Steps for this Generator:**
-   Currently only handles very simple assignment and return statements. Does not yet handle internal control flow (if/else, loops) or calls to other functions.
-   `expression_ast_repr` is a string representation; a richer, navigable AST substructure or a translation to a more formal expression language might be more powerful for AI reasoning.
-   `tags` field is currently static. Inferring relevant tags automatically is a future goal.
-   Relies on source code being available as a string; integrating with file system parsing is a next step.
-   "Parent module ID" is currently a placeholder.

## 6. Conclusion for this Experiment Phase

The hypothesis is validated for simple functions. AST parsing is a viable foundation for automated Holoform generation. The next logical step for this `task/auto-gen-v1` branch is to extend the `HoloformGeneratorVisitor` to recognize and represent **function calls** within the body of a parsed function.

*(End of Experiment Report)*