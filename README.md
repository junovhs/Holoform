# AI Research Project: Holoform - AI-Centric Codebase Abstraction

This repository hosts the artifacts and documentation for our AI-driven research project.

## Directory overview

- **experiments/**: experiment code and reports
- **data/**: datasets or links
- **models/**: trained model checkpoints and configs
- **results/**: aggregated metrics, plots and papers
- **notes/**: informal thinking and literature reviews
- **.github/workflows/**: CI for automated tests and linting

We track progress through meaningful commits, branches for major lines of work, and Git tags for milestones.

This repository hosts the research, experiments, code, and documentation for developing **Holoform**, an innovative system for creating AI-centric, token-efficient, and semantically rich abstractions of large codebases.

## Project Vision

The primary goal is to enable an Artificial Intelligence (AI) to efficiently navigate, understand, debug, and modify massive codebases (e.g., 400,000+ lines of code) by interacting with a condensed, structured, and multi-layered abstract representation—the Holoform—rather than raw source code directly. This aims to overcome AI token limitations and enhance reasoning capabilities for complex software engineering tasks.

## Key Research Areas

*   **Holoform Representation:** Designing data structures that can abstract various code constructs (functions, classes, modules, control flow, dependencies) while preserving essential semantic information.
*   **Automated Holoform Generation:** Developing programmatic methods (e.g., using AST parsing, static/dynamic analysis, potentially ML models) to automatically create Holoforms from source code.
*   **Holoform Interpretation & AI Interaction:** Building systems that allow an AI to "execute" or reason over Holoforms, trace dependencies, and use them for tasks like bug localization and code modification.
*   **Metrics & Evaluation:** Defining and applying metrics to assess the compression, fidelity, and utility of Holoforms for AI tasks.
*   **Scalability:** Ensuring the Holoform approach can scale to very large, real-world codebases.

## Directory Overview

*   **`src/`**: Source code for Holoform generators, interpreters, and related tools.
    *   **`src/holoform_generators/`**: Python package for AST-based Holoform generation.
*   **`experiments/`**: Detailed reports, configurations, and reproducible scripts for specific research experiments (e.g., testing a new Holoform feature, evaluating a generation technique).
*   **`data/`**: Sample code snippets used for testing, datasets for training future ML components (if any), or links to external codebases.
*   **`models/`**: (Future Use) Trained machine learning models if used for Holoform generation or analysis.
*   **`results/`**: Aggregated metrics, performance charts, and summary findings from experiments.
*   **`notes/`**: Informal thinking, literature reviews, brainstorming, and meeting notes.
*   **`.github/workflows/`**: CI/CD pipelines for automated linting, testing (when implemented), etc.

## Project Tracking

*   **`milestones.md`**: Defines high-level research goals and tracks their completion status.
*   **`RESEARCH_LOG.md`**: A chronological diary of research activities, key findings, decisions, and associated commits.

We track progress through meaningful commits, dedicated branches for major lines of work (e.g., `task/auto-gen-v1`), and Git tags for significant milestone completions.

## Current Status

The project has successfully completed **Milestones 1-5**, establishing a solid foundation for AI-centric code abstraction. Recent breakthrough experiments have demonstrated concrete evidence that Holoforms provide unique value for AI code understanding, particularly for:

- **Hidden State Modifications**: Making side effects explicit across function boundaries
- **Complex Control Flow**: Structuring nested conditions for clearer reasoning
- **Cross-Function Data Flow**: Showing explicit parameter mappings and data relationships
- **Token Efficiency**: Achieving ~50% token reduction with standard Holoforms and up to 97% with symbolic chain representations

These "magic moments" validate the core research hypothesis that Holoforms enable superior AI code comprehension compared to raw source code or AST representations. Our token efficiency experiments suggest that with further optimization, achieving 90-97% token reduction (3-10% of original usage) is a feasible goal.

## Next Phase

The research is now positioned to scale to larger codebases and explore advanced applications including extreme token efficiency optimization, GNN integration, multi-language support, and comprehensive user studies (Milestone 6).