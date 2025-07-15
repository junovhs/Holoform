# LLM Interaction Experiments

This document outlines the experiments for evaluating the effectiveness of the Holoform abstraction for LLM-based code understanding tasks.

## 1. Code Understanding Tasks

The following are the initial code understanding tasks that will be used to evaluate the LLM's performance:

1.  **Function Purpose:** Given the Holoform of a function, the LLM will be asked to explain the primary purpose of the function.
2.  **Variable Data Source:** Given the Holoform of a function and the name of a variable, the LLM will be asked to identify the data sources for that variable.
3.  **Bug Identification:** Given the Holoform of a function with a known bug, the LLM will be asked to identify the bug.

## 2. Prompt Templates

The following are the prompt templates that will be used for the experiments:

### 2.1. Function Purpose

```
Given the following Holoform, please explain the primary purpose of the function.

{holoform}
```

## 3. Success Criteria

The following are the success criteria for the LLM tasks:

*   **Function Purpose:** The LLM's response should accurately describe the function's purpose in a single sentence.
*   **Variable Data Source:** The LLM's response should correctly identify all the data sources for the variable.
*   **Bug Identification:** The LLM's response should correctly identify the bug in the function and provide a brief explanation of why it is a bug.

### 2.2. Variable Data Source

```
Given the following Holoform and variable name, please identify the data sources for the variable.

Holoform:
{holoform}

Variable:
{variable_name}
```

### 2.3. Bug Identification

```
Given the following Holoform, please identify the bug in the function.

{holoform}
```
