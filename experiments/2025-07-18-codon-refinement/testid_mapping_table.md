# TestID Mapping Table

**Purpose:** Cross-reference between test identifiers and original experiment data  
**Date:** July 18, 2025  
**Source:** July 2024 Validation Results Reanalysis

| TestID | Original Description | Pattern Category | Difficulty | Original Tokens | Compressed Tokens | Status |
|--------|---------------------|------------------|------------|-----------------|-------------------|---------|
| T1 | Context Scoping Logic | Scope Management | Intermediate | 62 | 22 | PASS |
| T2 | Error Recovery Flow | Error Handling | Advanced | 65 | 19 | PASS |
| T3 | Expert CLI Operation | Flow Control | Expert | 184 | 40 | PASS |
| T4 | Multi-Condition Decision Tree | Conditional Logic | Intermediate | 94 | 33 | PASS |
| T5 | Resource Management | Resource Management | Advanced | 86 | 24 | FAIL |
| T6 | Concurrent Context Handling | Scope Management | Advanced | 122 | 22 | PASS |
| T7 | Basic Git Operation | Flow Control | Basic | 71 | 16 | PASS |

## Summary Statistics

- **Total Tests:** 7
- **Pass Rate:** 6/7 (85.7%)
- **Failed Tests:** T5 (Resource Management)
- **Token Range:** 62-184 original, 16-40 compressed
- **Average Compression:** 72.7% (preliminary, before NCR calculation)

## Pattern Distribution

- **Flow Control:** 2 tests (T3, T7)
- **Scope Management:** 2 tests (T1, T6)
- **Error Handling:** 1 test (T2)
- **Conditional Logic:** 1 test (T4)
- **Resource Management:** 1 test (T5) - FAILED

## Difficulty Distribution

- **Basic:** 1 test (T7)
- **Intermediate:** 2 tests (T1, T4)
- **Advanced:** 3 tests (T2, T5, T6)
- **Expert:** 1 test (T3)

## Notes

- All baseline JSON files normalized to full schema compliance
- Dictionary tokens (D) = 107 (minimal dictionary)
- Original experiment date: January 17, 2024
- Reanalysis date: July 18, 2025