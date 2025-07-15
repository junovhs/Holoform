# Holoform Metrics

This document defines the metrics used to evaluate the effectiveness of the Holoform abstraction.

## 1. Semantic Compression Ratio

The Semantic Compression Ratio (SCR) measures how much smaller the Holoform representation is compared to the original source code, in terms of tokens. A higher SCR indicates a more token-efficient abstraction.

**Formula:**

```
SCR = (Source_Tokens - Holoform_Tokens) / Source_Tokens
```

Where:

*   `Source_Tokens`: The number of tokens in the original source code.
*   `Holoform_Tokens`: The number of tokens in the textual representation of the Holoform.

## 2. Semantic Fidelity Score

The Semantic Fidelity Score (SFS) measures how well the Holoform preserves the essential semantic information of the original source code. A higher SFS indicates a more faithful abstraction.

The SFS is calculated as a weighted average of the following sub-scores:

*   **Variable Preservation (40%):** Does the Holoform correctly identify all the variables in the original source code?
*   **Operation Preservation (30%):** Does the Holoform correctly identify all the operations in the original source code?
*   **Control Flow Preservation (20%):** Does the Holoform correctly represent the control flow of the original source code?
*   **Data Dependency Preservation (10%):** Does the Holoform correctly represent the data dependencies between variables?

Each sub-score is a value between 0 and 1, where 1 indicates perfect preservation and 0 indicates no preservation. The weights are chosen to reflect the relative importance of each sub-score.

## 3. Target Thresholds

The following are the initial target thresholds for the metrics:

*   **Semantic Compression Ratio (SCR):** > 0.5
*   **Semantic Fidelity Score (SFS):** > 0.8

These thresholds are a starting point and will be refined as the project progresses.

## 4. Falsification Thresholds

The following are the initial falsification thresholds for the project:

*   **If the SCR is consistently below 0.3 on the benchmark, the Holoform abstraction is not providing enough token efficiency.**
*   **If the SFS is consistently below 0.6 on the benchmark, the Holoform abstraction is not preserving enough semantic information.**

If these thresholds are not met, the current abstraction strategy will be re-evaluated.
