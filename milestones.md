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
*Goal: Develop a programmatic capability to generate basic Holoform structures directly from Python source code using Abstract Syntax Tree (AST) parsing, and establish foundational project infrastructure.*
*   **Sub-Task 2.1:** Develop initial AST visitor for simple Python functions (name, params, return, assignments, descriptions, semantic purpose). ✅
*   **Sub-Task 2.2:** Extend AST generator for internal function calls. ✅
*   **Sub-Task 2.3:** Extend AST generator for basic `for` loop structures. ✅
*   **Sub-Task 2.3.1 (Structural Refactor):** Refactor generator into a modular package. ✅
*   **Sub-Task 2.4:** Integrate auto-generated Holoforms into "Simulated Zero-In POC". ✅
*   **Sub-Task 2.5 (Infrastructure):** Configure GitHub Actions to run `src/holoform_generators/run_tests.py`. ✅
*   **Sub-Task 2.6 (Project Admin):** Add an OSI-approved open-source license file (e.g., MIT, Apache 2.0). ✅
*   **Sub-Task 2.7 (Project Admin):** Create a `CONTRIBUTING.md` file outlining contribution guidelines. ✅

## Milestone 3: Enhanced Representation, Metrics, & Initial LLM Interaction
*Goal: Enrich Holoform expressiveness for core language constructs, define robust evaluation metrics to address RQ1.1 (Fidelity/Loss) & RQ2.3 (Token Economics), and conduct initial LLM interaction experiments to explore RQ1.1, RQ1.2 (Comparative Efficacy), RQ4.1 (LLM Drift), & RQ4.2 (Explainability).*

*   **Sub-Task 3.0 (Conceptual & Documentation):**
    *   **M3.0.1 (Documentation):** Initiate and maintain `SPECIFICATION.md` for Holoform schema versions (ensures consistency for RQ evaluation). ✅
    *   **M3.0.2 (Design Foresight):** Outline high-level design considerations for multi-language support in `SPECIFICATION.md` or a dedicated design note (initial thoughts for RQ2.2). ✅

*   **Sub-Task 3.1: Holoform Representation for State Modifications (addresses RQ1.3 expressiveness for state)**
    *   **M3.1.1:** Analyze common patterns of state change in Python (e.g., attribute assignment, list/dict direct modifications). ✅
    *   **M3.1.2:** Design Holoform schema extensions (new operation types, fields for object ID, attribute/key, modification type) to represent these. Document in `SPECIFICATION.md`. ✅
    *   **M3.1.3:** Extend AST generator to parse and represent simple attribute assignments (`obj.attr = x`) and common list/dictionary direct modifications (e.g., `my_list.append()`, `my_dict['key'] = val`). ✅
    *   **M3.1.4:** Create test cases and validate Holoform generation for code involving these basic state changes. ✅

*   **Sub-Task 3.2: Holoform Representation for Classes and Methods (addresses RQ1.3 expressiveness for OOP)**
    *   **M3.2.1:** Design Holoform schema for classes (name, parent classes, methods list, class attributes) and methods (capturing `self`, linkage to class Holoform). Document in `SPECIFICATION.md`. ✅
    *   **M3.2.2:** Extend AST generator to parse `ClassDef` nodes, `FunctionDef` nodes within classes (methods), `__init__` methods (identifying instance attribute initializations like `self.x = ...`), and instance method calls (`my_object.do_something()`). ✅
    *   **M3.2.3:** Create test cases and validate Holoform generation for simple class definitions, instantiations, and method calls. ✅

*   **Sub-Task 3.3: Develop Robust Metrics for Holoform Evaluation (critical for RQ1.1, RQ2.3, RQ4.3)**
    *   **M3.3.1:** Define (with formula) and implement programmatic calculation for "Semantic Compression Ratio" (e.g., (Source Tokens - Textualized Holoform Tokens) / Source Tokens). ✅
    *   **M3.3.2:** Define (with criteria) and prototype programmatic calculation for a "Semantic Fidelity Score" (evaluating preservation of key operational elements like variables, operations, calls, control flow entry/exit points, and basic data dependencies from source). ✅
    *   **M3.3.3:** Develop/script tools to automate metric calculation on generated Holoforms. ✅
    *   **M3.3.4:** Establish a small, diverse benchmark set of Python code snippets/files for consistent metric evaluation across generator versions. ✅
    *   **M3.3.5:** Propose initial target thresholds or desirable ranges for these metrics, with justification. ✅
    *   **M3.3.6:** Define initial project falsification thresholds based on these metrics (e.g., "If compression < X% or fidelity < Y% on benchmark Z, current abstraction is insufficient") (addresses RQ4.3). ✅

*   **Sub-Task 3.4: Initial LLM Interaction with Textual Holoforms (foundational for RQ1.1, RQ1.2, RQ4.1, RQ4.2)**
    *   **M3.4.1:** Define 2-3 specific, simple code understanding or debugging tasks for LLM evaluation (e.g., "Explain the primary purpose of this function based on its Holoform," "Identify data sources for variable X in this Holoform operation"). ✅
    *   **M3.4.2:** Develop a consistent, human-readable textual serialization format for individual Holoforms suitable for LLM prompts. ✅
    *   **M3.4.3:** Design effective prompts for feeding the textual Holoform and the task query to an LLM. ✅
    *   **M3.4.4:** Conduct initial experiments by sending these prompts to a chosen LLM API. Document inputs, outputs, and LLM configurations. ✅
    *   **M3.4.5:** Qualitatively evaluate LLM responses for accuracy, relevance, and clarity against manually derived answers. Define simple success criteria for the tasks. ✅

## Milestone 4: Advanced Holoform Features, Inter-Holoform Analysis & Scalability
*Goal: Expand Holoform capabilities to cover more complex Python constructs (RQ1.3), enable robust analysis across multiple Holoforms (RQ2.1, RQ2.2, RQ2.3, RQ2.4), and begin addressing scalability and more complex dynamic aspects (RQ1.3).*

*   **Sub-Task 4.0 (Conceptual - Deeper Dive into Dynamic Semantics for RQ1.3):**
    *   **M4.0.1:** Investigate and document specific strategies for representing, abstracting, or at least annotating the presence of advanced runtime phenomena (e.g., dynamic method dispatch targets, reflection patterns, common concurrency idioms like `async/await`, significant I/O operations). Note limitations where full static representation is infeasible. Update `SPECIFICATION.md`. ✅

*   **Sub-Task 4.1: Comprehensive Control Flow Representation (addresses RQ1.3 expressiveness)**
    *   **M4.1.1:** Design and implement Holoform representation for `if/elif/else` structures (conditions, bodies, links). ✅
    *   **M4.1.2:** Design and implement Holoform representation for `while` loops (conditions, bodies). ✅
    *   **M4.1.3:** Design and implement Holoform representation for basic `try/except/finally` blocks (protected block, exception types, handlers). ✅
    *   **M4.1.4:** Extend AST generator and create comprehensive test cases for these control flow structures. ✅

*   **Sub-Task 4.2: Enhanced Data Flow Analysis (Intra-Holoform) (foundational for RQ1.1 fidelity & more precise discovery)**
    *   **M4.2.1:** Design schema extensions to represent more detailed intra-Holoform data dependencies (e.g., variable definition-use chains for all key variables). Update `SPECIFICATION.md`. ✅
    *   **M4.2.2:** Extend AST generator to accurately identify and store these data dependencies. ✅
    *   **M4.2.3:** Test data flow extraction accuracy. ✅

*   **Sub-Task 4.3: Inter-Holoform Call Graph & Project-Level Parsing (addresses RQ2.1, RQ2.2, RQ2.3)**
    *   **M4.3.1:** Develop functionality to parse all Python files from a specified project directory. ✅
    *   **M4.3.2:** Generate Holoforms for all supported functions and class methods found within the project. ✅
    *   **M4.3.3:** Construct and store a project-level Call Graph (nodes are Holoform IDs, edges are calls with parameter mapping details if possible). ✅
    *   **M4.3.4:** Enhance the "Simulated Zero-In POC" or create a new POC to use this project-level call graph for multi-hop traversal and dependency tracing across auto-generated Holoforms from different (simulated or actual) files. ✅

*   **Sub-Task 4.4: Scalability & Performance Profiling on Real Repositories (addresses RQ2.3, RQ2.4)**
    *   **M4.4.0:** Select and prepare 1-2 suitable open-source Python repositories (target 10k-50k LoC initially) as benchmarks. Document selection criteria. ✅
    *   **M4.4.1:** Successfully run Holoform generation (including project-level parsing and call graph construction from M4.3) on these benchmark repositories. ✅
    *   **M4.4.2:** Profile generator performance (total time, time per LoC/file, peak RAM usage, storage size for Holoforms & graph). Collect data for RQ2.3 (Token Economics) and RQ2.4 (Footprint). ✅
    *   **M4.4.3:** Identify and address any significant performance bottlenecks in the generator or graph construction. ✅

*   **Sub-Task 4.5 (Advanced Generator Feature - Incremental Updates for RQ2.1):**
    *   **M4.5.1:** Investigate and design a strategy for incremental Holoform regeneration (e.g., re-parsing only changed files and updating affected parts of the Holoform graph). ✅
    *   **M4.5.2:** Implement a basic prototype of this incremental update mechanism. ✅
    *   **M4.5.3:** Evaluate its performance benefits compared to full regeneration on a benchmark repo. ✅

## Milestone 5: Holoform-Native AI Reasoning & Advanced Applications
*Goal: Enable more sophisticated AI interaction with a structured Holoform database/graph and conduct experiments to answer core RQs (RQ1.1, RQ1.2, RQ3.1, RQ3.3, RQ4.2).*

*   **Sub-Task 5.0 (Advanced Evaluation - Loss Budget for RQ1.1):**
    *   **M5.0.1:** Design and conduct experiments to correlate Holoform fidelity levels (potentially by varying abstraction details) with LLM performance on selected downstream tasks (from M3.4 or new ones). This helps establish a "loss budget." ✅

*   **Sub-Task 5.1: Holoform Query Language/API (supports RQ4.1, RQ4.2 & enables advanced AI interaction)**
    *   **M5.1.1:** Research existing graph query languages and design a conceptual query language (e.g., a subset of Cypher-like syntax, or a fluent Python API) tailored for the Holoform graph structure and semantic attributes. ✅
    *   **M5.1.2:** Implement a prototype of this query API capable of executing common structural and semantic queries (e.g., "find all callers of X," "find Holoforms modifying data Y," "find paths between A and B under condition Z"). ✅

*   **Sub-Task 5.2: AI-Assisted Debugging with Holoform Graph (addresses RQ1.2, RQ3.1)**
    *   **M5.2.1:** Develop AI agent logic (simulated, or LLM using the Query API from M5.1) for more complex bug localization tasks using the project-level Holoform graph. ✅
    *   **M5.2.2:** Evaluate performance against baseline methods using a benchmark of publicly documented bugs (e.g., from Defects4J, or selected issues in benchmark repos from M4.4.0). ✅
    *   **M5.2.3 (Exploratory):** Investigate how to integrate simplified dynamic analysis information (e.g., execution traces from failing tests) to "highlight" or "weight" paths in the static Holoform graph for improved debugging accuracy (relevant to RQ1.3). ✅

*   **Sub-Task 5.3: Advanced Code Understanding & Summarization (addresses RQ1.2)**
    *   **M5.3.1:** Experiment with AI agents using the Query API (M5.1) to generate multi-Holoform summaries (e.g., summarizing a class's role based on its method Holoforms and their interactions, or module-level summaries). ✅
    *   **M5.3.2:** Compare the quality and utility of these summaries against baselines. ✅

*   **Sub-Task 5.4: (Exploratory) Holoforms for AI-Assisted Code Modification & Security Considerations**
    *   **M5.4.1:** Conceptualize how the Holoform graph and Query API could be used by an LLM to identify precise locations for code modifications and predict potential ripple effects (relevant to RQ4.2). ✅
    *   **M5.4.2 (Safety & Reliability):** Define a preliminary threat model for Holoform-guided AI code modification, focusing on how abstraction might lead to errors or overlook security implications (addresses RQ3.3). Document findings. ✅

---
## Future Research Directions (Milestone 6 and Beyond)

*Future research will focus on scaling Holoform to larger codebases, integrating with more advanced AI techniques, supporting multiple programming languages, and conducting user studies to evaluate real-world effectiveness. Key areas include:*

* Full-scale project analysis on >1MLoC codebases
* GNN integration for learning on Holoform graphs
* User Studies (RQ3.2)
* Deeper multi-language implementation (RQ2.2)
* IDE integration
* Advanced dynamic analysis integration