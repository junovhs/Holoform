# AIResearchProject/src/holoform_generators/test_code_strings.py

# --- Ground Truth Function variations for testing description extraction ---
G_HELPER_GT_CORRECT_CODE_STR_WITH_DOCSTRING = """
# This is a comment above the function - should be ignored if docstring exists.
def G_helper_gt_correct_docstring(val1, val2):
    '''This is the primary docstring description.
    It has multiple lines.
    And some    leading spaces on this line.'''
    result = (val1 * 2) + val2 # The core calculation for docstring test
    return result
"""

G_HELPER_GT_CORRECT_CODE_STR_WITH_COMMENT_ONLY = """
# Core utility: This is the comment description.
# It is on the line immediately above the function.
# And this comment also has multiple lines.
def G_helper_gt_correct_comment(val1, val2):
    # No docstring here
    result = (val1 * 2) + val2 # The inline comment for operation (comment test)
    return result
"""

G_HELPER_GT_CORRECT_CODE_STR_NO_COMMENT_OR_DOCSTRING = """
def G_helper_gt_correct_no_desc(val1, val2):
    result = (val1 * 2) + val2 # The core calculation for no_desc test
    return result
"""

# F_caller
F_CALLER_GT_CODE_STR = """
# Processes user input, then calls a helper, then adjusts result.
def F_caller_gt(f_input_x):
    '''This function demonstrates an internal call.
    It has pre-call and post-call logic.'''
    intermediate_val_f = f_input_x + 5 # Pre-call logic
    helper_result_f = G_helper_gt_correct_docstring(val1=f_input_x, val2=intermediate_val_f) # The function call
    final_output_f = helper_result_f + f_input_x # Post-call logic
    return final_output_f
"""

# Function with a Loop
F_WITH_LOOP_CODE_STR = """
def process_items_with_loop(item_list, factor):
    '''Processes each item in a list using a factor, accumulating results.'''
    accumulated_value = 0
    processed_items_details = [] # To store details from loop processing

    for item_value in item_list: # Loop over items
        processed_item = item_value * factor # Operation inside loop
        accumulated_value = accumulated_value + processed_item # Another operation inside loop

    final_result = accumulated_value + 10 # Final operation after loop
    return final_result 
"""

# --- Expected Holoform Description Parts for Validation ---
EXPECTED_H_G_HELPER_DOCSTRING_DESC_EXACT = """This is the primary docstring description.
    It has multiple lines.
    And some    leading spaces on this line."""
EXPECTED_H_G_HELPER_COMMENT_DESC = """# Core utility: This is the comment description.
# It is on the line immediately above the function.
# And this comment also has multiple lines."""

# --- Expected Operations Structures for Validation ---
EXPECTED_F_CALLER_OPERATIONS = [
    {
        "step_id": "s_assign_0", "expression_type": "arithmetic",
        "assign_to_variable": "intermediate_val_f",
        "expression_ast_repr": "BinOp(Name(id='f_input_x'), Add, Constant(value_type='number'))",
        "semantic_purpose": "Pre-call logic"
    },
    {
        "step_id": "s_assign_1", "type": "function_call",
        "assign_to_variable": "helper_result_f",
        "target_function_name": "G_helper_gt_correct_docstring",
        "parameter_mapping": {
            "val1": {"source_type": "variable", "name": "f_input_x"},
            "val2": {"source_type": "variable", "name": "intermediate_val_f"}
        },
        "semantic_purpose": "The function call"
    },
    {
        "step_id": "s_assign_2", "expression_type": "arithmetic",
        "assign_to_variable": "final_output_f",
        "expression_ast_repr": "BinOp(Name(id='helper_result_f'), Add, Name(id='f_input_x'))",
        "semantic_purpose": "Post-call logic", "assign_to_output": True 
    }
]

EXPECTED_F_WITH_LOOP_OPERATIONS = [
    {
        "step_id": "s_assign_0", "expression_type": "arithmetic", 
        "assign_to_variable": "accumulated_value", 
        "expression_ast_repr": "Constant(value_type='number')", 
        "semantic_purpose": "Assign value to 'accumulated_value'" 
    },
    {
        "step_id": "s_assign_1", "expression_type": "list_literal", 
        "assign_to_variable": "processed_items_details",
        "expression_ast_repr": "List(elts=[])", 
        "semantic_purpose": "Assign value to 'processed_items_details'"
    },
    {
        "step_id": "s_loop_2", 
        "type": "for_loop",
        "target_variable": "item_value",
        "iterable_source_repr": "Name(id='item_list')",
        "semantic_purpose": "Loop over items",
        "loop_body_operations": [
            {
                "step_id": "s_loop_assign_0", "expression_type": "arithmetic",
                "assign_to_variable": "processed_item",
                "expression_ast_repr": "BinOp(Name(id='item_value'), Mult, Name(id='factor'))",
                "semantic_purpose": "Operation inside loop"
            },
            {
                "step_id": "s_loop_assign_1", "expression_type": "arithmetic",
                "assign_to_variable": "accumulated_value",
                "expression_ast_repr": "BinOp(Name(id='accumulated_value'), Add, Name(id='processed_item'))",
                "semantic_purpose": "Another operation inside loop"
            }
        ]
    },
    {
        "step_id": "s_assign_3", "expression_type": "arithmetic",
        "assign_to_variable": "final_result",
        "expression_ast_repr": "BinOp(Name(id='accumulated_value'), Add, Constant(value_type='number'))", 
        "semantic_purpose": "Final operation after loop",
        "assign_to_output": True 
    }
]
