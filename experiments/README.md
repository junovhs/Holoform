# Experiments Directory

This directory contains documentation and supporting materials for specific research experiments conducted as part of the Holoform project.

## Structure:

Each distinct experiment or significant Proof-of-Concept (POC) validation should be documented in its own sub-folder or markdown file.

*   **Naming Convention:** Use a clear, chronological, and descriptive naming convention, for example:
    *   `exp-YYYYMMDD-ast-generator-function-calls/` (for a folder)
    *   `exp-20240523-simulated-zero-in-poc.md` (for a markdown file, like the one you created)

## Experiment Documentation:

Each experiment's documentation (whether a dedicated folder with a `report.md` or a single markdown file) should aim to include:

1.  **Overview:**
    *   Date of the experiment.
    *   Associated Git branch(es) and key commit hash(es).
    *   Purpose of the experiment and the specific hypothesis being tested.
2.  **Configuration:**
    *   Description of the code/tools used (e.g., version of the Holoform generator, interpreter).
    *   Input data (e.g., specific Python code snippets, types of Holoforms used).
    *   Any specific parameters or settings for the experiment.
3.  **Process / Methodology:**
    *   A clear description of the steps taken during the experiment.
4.  **Results & Metrics:**
    *   Quantitative results (e.g., Behavioral Fidelity Scores, Pinpointing Accuracy, Token Efficiency metrics).
    *   Qualitative results (e.g., analysis of generated Holoform structures, quality of AI-generated explanations).
    *   Tables and charts where appropriate.
5.  **Analysis & Discussion:**
    *   Interpretation of the results.
    *   What worked, what didn't, and why.
    *   Comparison to baselines or previous experiments, if applicable.
6.  **Conclusion & Next Steps:**
    *   Was the hypothesis validated?
    *   What are the implications for the Holoform project?
    *   What are the recommended next steps or future experiments based on these findings?

Refer to `template_experiment.md` for a starting point for new experiment reports.

Commit all resources related to a single experiment together. Once an experiment yields significant, stable findings, its branch can be merged, and the corresponding commit on `main` can be tagged if it represents a milestone achievement.