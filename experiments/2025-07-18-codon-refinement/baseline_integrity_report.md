# Baseline Integrity Report

**Date:** July 18, 2025  
**Purpose:** Verify all baseline JSON files contain required schema fields  
**Schema Version:** Raw Data Schema v1.0

## Field Requirements Checklist

Required fields per Raw Data Schema:
- `test_id` (string)
- `date` (ISO date string)
- `pattern_sequence` (string description)
- `O` (integer - original tokens)
- `C` (integer - compressed tokens)
- `D` (integer - dictionary tokens)
- `dict_version` (string)
- `k` (integer - amortization factor)
- `baseline_questions` (array)
- `baseline_correct` (integer or null)
- `compressed_correct` (integer or null)
- `semantic_units_total` (integer)
- `semantic_units_recovered` (integer or null)
- `error_paths_total` (integer)
- `error_paths_recovered` (integer or null)
- `notes` (string)

## Test File Integrity Status

### T1.json ✅ COMPLIANT
- ✅ test_id: "T1"
- ✅ date: "2024-01-17"
- ✅ pattern_sequence: "Context Scoping Logic (Intermediate)"
- ✅ O: 62
- ✅ C: 22
- ✅ D: 107
- ✅ dict_version: "v2.0-2025-07-18"
- ✅ k: 1
- ✅ baseline_questions: [4 questions]
- ✅ baseline_correct: null
- ✅ compressed_correct: null
- ✅ semantic_units_total: 4
- ✅ semantic_units_recovered: null
- ✅ error_paths_total: 0
- ✅ error_paths_recovered: null
- ✅ notes: present

### T2.json ✅ COMPLIANT
- ✅ test_id: "T2"
- ✅ date: "2024-01-17"
- ✅ pattern_sequence: "Error Recovery Flow (Advanced)"
- ✅ O: 65
- ✅ C: 19
- ✅ D: 107
- ✅ dict_version: "v2.0-2025-07-18"
- ✅ k: 1
- ✅ baseline_questions: [4 questions]
- ✅ baseline_correct: null
- ✅ compressed_correct: null
- ✅ semantic_units_total: 4
- ✅ semantic_units_recovered: null
- ✅ error_paths_total: 2
- ✅ error_paths_recovered: null
- ✅ notes: present

### T3.json ✅ COMPLIANT
- ✅ test_id: "T3"
- ✅ date: "2024-01-17"
- ✅ pattern_sequence: "Expert CLI Operation"
- ✅ O: 184
- ✅ C: 40
- ✅ D: 107
- ✅ dict_version: "v2.0-2025-07-18"
- ✅ k: 1
- ✅ baseline_questions: [5 questions]
- ✅ baseline_correct: null
- ✅ compressed_correct: null
- ✅ semantic_units_total: 5
- ✅ semantic_units_recovered: null
- ✅ error_paths_total: 1
- ✅ error_paths_recovered: null
- ✅ notes: present

### T4.json ✅ COMPLIANT
- ✅ test_id: "T4"
- ✅ date: "2024-01-17"
- ✅ pattern_sequence: "Multi-Condition Decision Tree"
- ✅ O: 94
- ✅ C: 33
- ✅ D: 107
- ✅ dict_version: "v2.0-2025-07-18"
- ✅ k: 1
- ✅ baseline_questions: [4 questions]
- ✅ baseline_correct: null
- ✅ compressed_correct: null
- ✅ semantic_units_total: 4
- ✅ semantic_units_recovered: null
- ✅ error_paths_total: 0
- ✅ error_paths_recovered: null
- ✅ notes: present

### T5.json ✅ COMPLIANT
- ✅ test_id: "T5"
- ✅ date: "2024-01-17"
- ✅ pattern_sequence: "Resource Management (FAILED)"
- ✅ O: 86
- ✅ C: 24
- ✅ D: 107
- ✅ dict_version: "v2.0-2025-07-18"
- ✅ k: 1
- ✅ baseline_questions: [4 questions]
- ✅ baseline_correct: null
- ✅ compressed_correct: null
- ✅ semantic_units_total: 4
- ✅ semantic_units_recovered: null
- ✅ error_paths_total: 2
- ✅ error_paths_recovered: null
- ✅ notes: present

### T6.json ✅ COMPLIANT
- ✅ test_id: "T6"
- ✅ date: "2024-01-17"
- ✅ pattern_sequence: "Concurrent Context Handling"
- ✅ O: 122
- ✅ C: 22
- ✅ D: 107
- ✅ dict_version: "v2.0-2025-07-18"
- ✅ k: 1
- ✅ baseline_questions: [4 questions]
- ✅ baseline_correct: null
- ✅ compressed_correct: null
- ✅ semantic_units_total: 4
- ✅ semantic_units_recovered: null
- ✅ error_paths_total: 1
- ✅ error_paths_recovered: null
- ✅ notes: present

### T7.json ✅ COMPLIANT
- ✅ test_id: "T7"
- ✅ date: "2024-01-17"
- ✅ pattern_sequence: "Basic Git Operation"
- ✅ O: 71
- ✅ C: 16
- ✅ D: 107
- ✅ dict_version: "v2.0-2025-07-18"
- ✅ k: 1
- ✅ baseline_questions: [3 questions]
- ✅ baseline_correct: null
- ✅ compressed_correct: null
- ✅ semantic_units_total: 3
- ✅ semantic_units_recovered: null
- ✅ error_paths_total: 0
- ✅ error_paths_recovered: null
- ✅ notes: present

## Summary

**Overall Status:** ✅ ALL COMPLIANT  
**Total Files:** 7  
**Compliant Files:** 7  
**Non-Compliant Files:** 0

## Data Consistency Checks

- ✅ All files use consistent dictionary version: "v2.0-2025-07-18"
- ✅ All files use consistent D value: 107 (minimal dictionary)
- ✅ All files use consistent k value: 1 (single use amortization)
- ✅ All files use consistent date: "2024-01-17"
- ✅ All null fields properly marked for future population
- ✅ Semantic units and error paths counts are reasonable

## Schema Updates

**Minor schema patch applied on 2025-07-18:**
- Added `dict_mode` field (value: "minimal")
- Added `dictionary_hash` field (SHA256: 8c1f63e2...)
- Added `k_single` and `k_batch` fields for amortization tracking
- All files remain fully compliant with extended schema

## Data Consistency Checks

- ✅ All files use consistent dictionary version: "v2.0-2025-07-18"
- ✅ All files use consistent D value: 107 (minimal dictionary)
- ✅ All files use consistent k value: 1 (single use amortization)
- ✅ All files use consistent date: "2024-01-17"
- ✅ All null fields properly marked for future population
- ✅ Semantic units and error paths counts are reasonable

## Ready for Phase 3

All baseline JSON files are properly normalized and schema-compliant. Ready to proceed with NCR calculations and Phase 3 processing.

**Next Step:** Phase 3 - Dictionary Overhead & NCR computation