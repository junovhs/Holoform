# Research Milestones: AI-Centric Codebase Abstraction (Holoform)

## Milestone 1: Foundational Holoform Principles & POCs (Conceptual Validation)
*Goal: Validate core Holoform concepts for abstract representation, interpretation, and AI-assisted reasoning on small, illustrative code examples, with manually crafted Holoforms.*
*   Defined initial Holoform concept for linear transformations (Math POC). ✅
*   Implemented and tested Math POC for execution, impact analysis, and bug detection. ✅
*   Defined Holoform structure for simple conditional logic (Conditional POC v1). ✅
*   Implemented and tested Conditional POC v1, including behavioral fidelity metrics. ✅
*   Defined Holoform structure for inter-function calls (Inter-Holoform Call POC v1 - manual Holoforms). ✅
*   Implemented and tested Inter-Holoform Call POC v1 for behavioral fidelity using manual Holoforms. ✅
*   Incorporated research survey insights into Holoform strategy and potential metrics. ✅
*   Defined Holoform POC for Simulated Zero-In (Search + Traversal with manual Holoforms) (POC v2). ✅
*   Implemented and tested "Simulated Zero-In with Graph-Contextualized Holoform Traversal & Explainable Pinpointing" (POC v2), including qualitative explainability metric, using manual Holoforms. ✅

## Milestone 2: Basic Automated Holoform Generation (AST-Based)
*Goal: Develop a programmatic capability to generate basic Holoform structures directly from Python source code using Abstract Syntax Tree (AST) parsing.*
*   **Sub-Task 2.1:** Develop initial AST visitor to parse simple, self-contained Python functions (`G_helper` variants) and extract: ✅
    *   Function name and input parameters.
    *   Return variable.
    *   Simple assignment operations and their expression structure (as AST string representation).
    *   Function description (from docstrings or preceding comments).
    *   Operation semantic purpose (from inline comments).
*   **Sub-Task 2.2 (Current Focus):** Extend AST generator to identify and represent internal function calls within a parsed function's body (e.g., for `F_caller_gt` calling `G_helper_gt`). 🔲
*   **Sub-Task 2.3:** Handle basic loop structures (e.g., a simple `for` loop) in the AST generator. 🔲
*   **Sub-Task 2.4:** Integrate auto-generated Holoforms from 2.1 & 2.2 into the "Simulated Zero-In POC" to verify end-to-end flow with generated abstractions. 🔲

## Milestone 3: Enhanced Holoform Representation & AI Interaction
*Goal: Enrich Holoform expressiveness and explore direct interaction with LLMs.*
*   Design Holoform representation for basic state modifications. 🔲
*   Design Holoform representation for classes and methods. 🔲
*   Develop more robust metrics for Holoform "compression" (semantic density) and "fidelity". 🔲
*   Experiment with feeding generated Holoforms (textual representation) to an LLM for specific debugging or understanding tasks, evaluating its performance. 🔲

_(Future Milestones: Scalability, GNN integration, UI-specific adaptations, etc.)_