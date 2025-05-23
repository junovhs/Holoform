# Contributing to Holoform

First off, thank you for considering contributing to Holoform! Your help is appreciated.

## How to Contribute

Currently, the project is in its early research and development stages. Here are some ways you could contribute:

*   **Reporting Bugs:** If you find a bug in the Holoform generator or other parts of the project, please open an issue on GitHub. Describe the bug, how to reproduce it, and what you expected to happen.
*   **Suggesting Enhancements:** If you have ideas for new features or improvements to existing ones, feel free to open an issue to discuss it.
*   **Code Contributions (Future):** While we are still defining the core architecture, code contributions will be welcome in the future. Please generally:
    *   Open an issue to discuss any significant changes you'd like to make before starting the work.
    *   Follow the existing code style (details to be added).
    *   Ensure any new code includes relevant tests.
    *   Create a Pull Request for your changes.

## Setting up a Development Environment

1.  Clone the repository: `git clone https://github.com/junovhs/Holoform.git`
2.  Navigate to the project directory: `cd Holoform`
3.  It's recommended to use a Python virtual environment.

    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate

4.  (No external dependencies to install yet beyond standard Python)

## Running Tests

Tests for the Holoform generator are located in `src/holoform_generators/` and can be run using:

python src/holoform_generators/run_tests.py
Please ensure all tests pass before submitting a pull request.
Code of Conduct
While we don't have a formal Code of Conduct document yet, please be respectful and constructive in all interactions within the project community.
Thank you for your interest in Holoform!