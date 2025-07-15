# AIResearchProject/src/holoform_generators/run_tests.py
import json
import sys # <--- ADDED IMPORT SYS
import os

# --- START Workaround for imports when run as a script ---
_CURRENT_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_SRC_DIR = os.path.dirname(_CURRENT_SCRIPT_DIR) 
_PROJECT_ROOT_DIR = os.path.dirname(_SRC_DIR)    

if _PROJECT_ROOT_DIR not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT_DIR)

from src.holoform_generators.main_generator import generate_holoform_from_code_string
from src.holoform_generators.validation_utils import compare_holoforms
from src.holoform_generators import test_code_strings as tcs
from src.holoform_generators import constants as C
# --- END Workaround ---

def run_all_tests():
    test_suite_results = []
    passed_all = True

    # --- Test Case 1: G_helper_gt_correct_docstring ---
    test_name_1 = "G_helper_gt_correct_docstring"
    expected_operations_g_helper_docstring = [
        {
            "step_id": "s_assign_0",
            "expression_type": "arithmetic",
            "assign_to_variable": "result",
            "expression_ast_repr": "BinOp(BinOp(Name(id='val1'), Mult, Constant(value_type='number')), Add, Name(id='val2'))",
            "semantic_purpose": "The core calculation for docstring test",
            "assign_to_output": True
        }
    ]
    expected_desc_1_cleaned = "This is the primary docstring description.\n    It has multiple lines.\n    And some    leading spaces on this line."
    expected_holoform_1 = {
        "id": "G_helper_gt_correct_docstring_auto_v1",
        "description": expected_desc_1_cleaned, 
        "input_parameters": ["val1", "val2"],
        "output_variable_name": "result",
        "operations": expected_operations_g_helper_docstring,
        "parent_module_id": C.DEFAULT_PARENT_MODULE_ID, 
        "tags": list(C.DEFAULT_TAGS) 
    }
    print(f"\n--- Running Test: {test_name_1} ---")
    generated_holoform_1 = generate_holoform_from_code_string(
        tcs.G_HELPER_GT_CORRECT_CODE_STR_WITH_DOCSTRING,
        "G_helper_gt_correct_docstring"
    )
    result_1 = compare_holoforms(generated_holoform_1, expected_holoform_1)
    test_suite_results.append({"name": test_name_1, "passed": result_1})
    if not result_1: passed_all = False
    print(f"--- Test {test_name_1} {'PASSED' if result_1 else 'FAILED'} ---")

    # --- Test Case 2: G_helper_gt_correct_comment ---
    test_name_2 = "G_helper_gt_correct_comment"
    expected_desc_2_cleaned = """Core utility: This is the comment description.
It is on the line immediately above the function.
And this comment also has multiple lines."""
    expected_operations_g_helper_comment = [
        {
            "step_id": "s_assign_0",
            "expression_type": "arithmetic",
            "assign_to_variable": "result",
            "expression_ast_repr": "BinOp(BinOp(Name(id='val1'), Mult, Constant(value_type='number')), Add, Name(id='val2'))",
            "semantic_purpose": "The inline comment for operation (comment test)",
            "assign_to_output": True
        }
    ]
    expected_holoform_2 = {
        "id": "G_helper_gt_correct_comment_auto_v1",
        "description": expected_desc_2_cleaned, 
        "input_parameters": ["val1", "val2"],
        "output_variable_name": "result",
        "operations": expected_operations_g_helper_comment
    }
    print(f"\n--- Running Test: {test_name_2} ---")
    generated_holoform_2 = generate_holoform_from_code_string(
        tcs.G_HELPER_GT_CORRECT_CODE_STR_WITH_COMMENT_ONLY,
        "G_helper_gt_correct_comment"
    )
    result_2 = compare_holoforms(generated_holoform_2, expected_holoform_2)
    test_suite_results.append({"name": test_name_2, "passed": result_2})
    if not result_2: passed_all = False
    print(f"--- Test {test_name_2} {'PASSED' if result_2 else 'FAILED'} ---")

    # --- Test Case 3: G_helper_gt_correct_no_desc ---
    test_name_3 = "G_helper_gt_correct_no_desc"
    expected_default_desc = "Func 'G_helper_gt_correct_no_desc_auto_v1' for 'The core calculation for no_desc test'."
    expected_operations_g_helper_no_desc = [
        {
            "step_id": "s_assign_0",
            "expression_type": "arithmetic",
            "assign_to_variable": "result",
            "expression_ast_repr": "BinOp(BinOp(Name(id='val1'), Mult, Constant(value_type='number')), Add, Name(id='val2'))",
            "semantic_purpose": "The core calculation for no_desc test",
            "assign_to_output": True
        }
    ]
    expected_holoform_3 = {
        "id": "G_helper_gt_correct_no_desc_auto_v1",
        "description": expected_default_desc,
        "input_parameters": ["val1", "val2"],
        "output_variable_name": "result",
        "operations": expected_operations_g_helper_no_desc
    }
    print(f"\n--- Running Test: {test_name_3} ---")
    generated_holoform_3 = generate_holoform_from_code_string(
        tcs.G_HELPER_GT_CORRECT_CODE_STR_NO_COMMENT_OR_DOCSTRING,
        "G_helper_gt_correct_no_desc"
    )
    result_3 = compare_holoforms(generated_holoform_3, expected_holoform_3)
    test_suite_results.append({"name": test_name_3, "passed": result_3})
    if not result_3: passed_all = False
    print(f"--- Test {test_name_3} {'PASSED' if result_3 else 'FAILED'} ---")

    # --- Test Case 4: F_caller_gt ---
    test_name_4 = "F_caller_gt"
    expected_f_caller_docstring_cleaned = """This function demonstrates an internal call.
    It has pre-call and post-call logic."""
    expected_holoform_4 = {
        "id": "F_caller_gt_auto_v1",
        "description": expected_f_caller_docstring_cleaned, 
        "input_parameters": ["f_input_x"],
        "output_variable_name": "final_output_f",
        "operations": tcs.EXPECTED_F_CALLER_OPERATIONS
    }
    print(f"\n--- Running Test: {test_name_4} ---")
    generated_holoform_4 = generate_holoform_from_code_string(
        tcs.F_CALLER_GT_CODE_STR,
        "F_caller_gt"
    )
    result_4 = compare_holoforms(generated_holoform_4, expected_holoform_4)
    test_suite_results.append({"name": test_name_4, "passed": result_4})
    if not result_4: passed_all = False
    print(f"--- Test {test_name_4} {'PASSED' if result_4 else 'FAILED'} ---")
    
    # --- Test Case 5: F_with_loop_gt ---
    test_name_5 = "F_with_loop_gt"
    expected_f_with_loop_docstring_cleaned = "Processes each item in a list using a factor, accumulating results."
    expected_holoform_5 = {
        "id": "process_items_with_loop_auto_v1",
        "description": expected_f_with_loop_docstring_cleaned, 
        "input_parameters": ["item_list", "factor"],
        "output_variable_name": "final_result",
        "operations": tcs.EXPECTED_F_WITH_LOOP_OPERATIONS 
    }
    print(f"\n--- Running Test: {test_name_5} ---")
    generated_holoform_5 = generate_holoform_from_code_string(
        tcs.F_WITH_LOOP_CODE_STR,
        "process_items_with_loop"
    )
    result_5 = compare_holoforms(generated_holoform_5, expected_holoform_5)
    test_suite_results.append({"name": test_name_5, "passed": result_5})
    if not result_5: passed_all = False
    print(f"--- Test {test_name_5} {'PASSED' if result_5 else 'FAILED'} ---")

    # --- Test Case 6: State Modification ---
    test_name_6 = "State_Modification"
    expected_holoform_6 = {
        "id": "process_data_auto_v1",
        "description": "Func 'process_data_auto_v1' for 'Call & assign to 'my_obj''.",
        "input_parameters": ["data_dict", "items_list"],
        "output_variable_name": None,
        "operations": tcs.EXPECTED_STATE_MODIFICATION_OPERATIONS,
        "parent_module_id": C.DEFAULT_PARENT_MODULE_ID,
        "tags": list(C.DEFAULT_TAGS)
    }
    print(f"\n--- Running Test: {test_name_6} ---")
    generated_holoform_6 = generate_holoform_from_code_string(
        tcs.STATE_MODIFICATION_CODE_STR,
        "process_data"
    )
    result_6 = compare_holoforms(generated_holoform_6, expected_holoform_6)
    test_suite_results.append({"name": test_name_6, "passed": result_6})
    if not result_6: passed_all = False
    print(f"--- Test {test_name_6} {'PASSED' if result_6 else 'FAILED'} ---")

    # --- Test Case 7: Class Definition ---
    test_name_7 = "Class_Definition"
    print(f"\n--- Running Test: {test_name_7} ---")
    generated_holoform_7 = generate_holoform_from_code_string(
        tcs.CLASS_METHOD_CODE_STR,
        "MyTestClass"
    )
    result_7 = compare_holoforms(generated_holoform_7, tcs.EXPECTED_CLASS_HOLOFORM)
    test_suite_results.append({"name": test_name_7, "passed": result_7})
    if not result_7: passed_all = False
    print(f"--- Test {test_name_7} {'PASSED' if result_7 else 'FAILED'} ---")

    # --- Test Case 8: Use Class ---
    test_name_8 = "Use_Class"
    expected_holoform_8 = {
        "id": "use_class_auto_v1",
        "description": "Func 'use_class_auto_v1' for 'Call & assign to 'my_instance''.",
        "input_parameters": [],
        "output_variable_name": None,
        "operations": tcs.EXPECTED_USE_CLASS_OPERATIONS
    }
    print(f"\n--- Running Test: {test_name_8} ---")
    generated_holoform_8 = generate_holoform_from_code_string(
        tcs.CLASS_METHOD_CODE_STR,
        "use_class"
    )
    result_8 = compare_holoforms(generated_holoform_8, expected_holoform_8)
    test_suite_results.append({"name": test_name_8, "passed": result_8})
    if not result_8: passed_all = False
    print(f"--- Test {test_name_8} {'PASSED' if result_8 else 'FAILED'} ---")

    # --- Summary ---
    print("\n\n--- Test Suite Summary ---")
    num_passed = sum(1 for r in test_suite_results if r["passed"])
    num_total = len(test_suite_results)
    print(f"Passed {num_passed}/{num_total} tests.")

    if not passed_all:
        print("\nDetails of FAILED tests (see specific outputs above):")
        for r_idx, r_val in enumerate(test_suite_results):
            if not r_val["passed"]:
                print(f"- Test {r_idx+1}: {r_val['name']} FAILED")
    else:
        print("All tests passed successfully!")
    
    return passed_all

if __name__ == "__main__":
    all_tests_passed = run_all_tests()
    if not all_tests_passed:
        print("\nSome tests FAILED. Please review the output above for details.")
        sys.exit(1) # <--- ADDED SYS.EXIT(1) FOR CI
    else:
        print("\nAll tests in run_tests.py PASSED.")