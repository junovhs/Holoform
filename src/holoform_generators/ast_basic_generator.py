# AIResearchProject/src/holoform_generators/ast_basic_generator.py
import ast
import json
import inspect 
import re 

# --- Ground Truth Function variations for testing ---
# G_helper variants (unchanged from previous version)
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

# F_caller (unchanged from previous version)
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

# NEW Ground Truth Function with a Loop
F_WITH_LOOP_CODE_STR = """
def process_items_with_loop(item_list, factor):
    '''Processes each item in a list using a factor, accumulating results.'''
    accumulated_value = 0
    processed_items_details = [] # To store details from loop processing

    for item_value in item_list: # Loop over items
        processed_item = item_value * factor # Operation inside loop
        accumulated_value = accumulated_value + processed_item # Another operation inside loop
        # Conceptual call inside loop for richer testing:
        # log_details = G_helper_gt_correct_docstring(processed_item, item_value) 
        # processed_items_details.append(log_details) # Appending result of a call

    # Final operation after loop
    final_result = accumulated_value + 10 
    return final_result 
    # Intentionally not returning processed_items_details to keep output simple for now
"""


# --- Expected Holoform Parts for Validation (some unchanged) ---
EXPECTED_H_G_HELPER_DOCSTRING_DESC_EXACT = """This is the primary docstring description.
    It has multiple lines.
    And some    leading spaces on this line."""
EXPECTED_H_G_HELPER_COMMENT_DESC = "Core utility: This is the comment description.\nIt is on the line immediately above the function.\nAnd this comment also has multiple lines."

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
    { # accumulated_value = 0
        "step_id": "s_assign_0", "expression_type": "arithmetic", 
        "assign_to_variable": "accumulated_value", 
        "expression_ast_repr": "Constant(value_type='number')", # For 0
        "semantic_purpose": "Assign value to 'accumulated_value'" 
    },
    { # processed_items_details = []
        "step_id": "s_assign_1", "expression_type": "list_literal", # New type maybe
        "assign_to_variable": "processed_items_details",
        "expression_ast_repr": "List(elts=[])", # AST for empty list
        "semantic_purpose": "Assign value to 'processed_items_details'"
    },
    { # for item_value in item_list:
        "step_id": "s_loop_2", # Index might change based on op counter
        "type": "for_loop",
        "target_variable": "item_value",
        "iterable_source_repr": "Name(id='item_list')",
        "semantic_purpose": "Loop over items",
        "loop_body_operations": [
            { # processed_item = item_value * factor
                "step_id": "s_loop_assign_0", "expression_type": "arithmetic",
                "assign_to_variable": "processed_item",
                "expression_ast_repr": "BinOp(Name(id='item_value'), Mult, Name(id='factor'))",
                "semantic_purpose": "Operation inside loop"
            },
            { # accumulated_value = accumulated_value + processed_item
                "step_id": "s_loop_assign_1", "expression_type": "arithmetic",
                "assign_to_variable": "accumulated_value",
                "expression_ast_repr": "BinOp(Name(id='accumulated_value'), Add, Name(id='processed_item'))",
                "semantic_purpose": "Another operation inside loop"
            }
            # Calls inside loop are more complex to add now, deferring for this iteration if too tricky.
        ]
    },
    { # final_result = accumulated_value + 10
        "step_id": "s_assign_3", "expression_type": "arithmetic",
        "assign_to_variable": "final_result",
        "expression_ast_repr": "BinOp(Name(id='accumulated_value'), Add, Constant(value_type='number'))", # for 10
        "semantic_purpose": "Final operation after loop",
        "assign_to_output": True # Because 'final_result' is returned
    }
]


# --- AST Node Visitor Class (Revised to handle 'for' loops) ---
class HoloformGeneratorVisitor(ast.NodeVisitor):
    def __init__(self, source_code_lines_list):
        self.source_lines = source_code_lines_list
        self.holoform_data = {
            "id": "", "parent_module_id": "Unknown_Module_AST_v1", 
            "description": "Auto-generated Holoform (default description).",
            "tags": ["ast_generated"], "input_parameters": [],
            "operations": [], "output_variable_name": None
        }
        self.current_op_idx = 0
        self.is_in_loop_body = False # Flag to adjust op_id prefix if needed

    def _get_comment_block_above_node(self, node_lineno): # Unchanged
        if node_lineno <= 1: return None
        comment_block_lines = []
        current_line_idx = node_lineno - 2 
        while current_line_idx >= 0:
            line_content = self.source_lines[current_line_idx].strip()
            original_line_content = self.source_lines[current_line_idx]
            if line_content.startswith("#"): comment_block_lines.insert(0, original_line_content) 
            elif not line_content: 
                if comment_block_lines: break 
            else: break
            current_line_idx -= 1
        return "\n".join(comment_block_lines) if comment_block_lines else None

    def visit_FunctionDef(self, node): # Unchanged, but calls new visit_For
        self.holoform_data["id"] = f"{node.name}_auto_v1"
        docstring = ast.get_docstring(node, clean=False) 
        if docstring: self.holoform_data["description"] = docstring
        else:
            comments_above = self._get_comment_block_above_node(node.lineno)
            if comments_above: self.holoform_data["description"] = comments_above
        
        for arg in node.args.args: self.holoform_data["input_parameters"].append(arg.arg)
        
        self._process_body_nodes(node.body) # Refactored body processing

    def _process_body_nodes(self, body_nodes_list, current_operations_list=None):
        """Helper to process a list of body nodes (for func body or loop body)."""
        if current_operations_list is None:
             # This means we are processing the main function body
            current_operations_list = self.holoform_data["operations"]
        
        original_in_loop_body_state = self.is_in_loop_body # Save state

        for body_item_idx, body_item in enumerate(body_nodes_list):
            # Skip docstring if it's the first item in function body
            if not self.is_in_loop_body and body_item_idx == 0 and isinstance(body_item, ast.Expr) and \
               isinstance(body_item.value, ast.Constant) and \
               isinstance(body_item.value.value, str) and ast.get_docstring(body_nodes_list[0].parent if hasattr(body_nodes_list[0],'parent') else body_nodes_list[0] , clean=False): # Check if it is a docstring of the parent
                continue 
            elif isinstance(body_item, ast.Assign):
                # Pass the list where the new operation should be appended
                self.visit_Assign(body_item, target_operations_list=current_operations_list)
            elif isinstance(body_item, ast.Return):
                self.visit_Return(body_item, source_operations_list=current_operations_list)
            elif isinstance(body_item, ast.For):
                self.visit_For(body_item, target_operations_list=current_operations_list)
            elif isinstance(body_item, ast.Expr) and isinstance(body_item.value, ast.Call):
                self.visit_Call_Standalone(body_item.value, target_operations_list=current_operations_list)


        self.is_in_loop_body = original_in_loop_body_state # Restore state

    def _get_step_id(self, prefix_override=None):
        if self.is_in_loop_body:
            # For operations inside a loop, might want a different prefix or counter system.
            # For now, we'll use a simple counter managed by loop, if any, or a generic one
             return f"s_loop_{prefix_override if prefix_override is not None else 'op'}_{self.loop_op_idx if hasattr(self, 'loop_op_idx') else self.current_op_idx}"
        return f"s_{prefix_override if prefix_override else 'assign'}_{self.current_op_idx}"


    def _ast_node_to_repr_str(self, node): # Updated to include List
        if isinstance(node, ast.Name): return f"Name(id='{node.id}')"
        elif isinstance(node, ast.Constant):
            val_type = type(node.value).__name__
            if isinstance(node.value, (int, float)): val_type = 'number' 
            elif isinstance(node.value, list) and not node.value : return "List(elts=[])" # Handle empty list constant
            return f"Constant(value_type='{val_type}')" 
        elif isinstance(node, ast.Num): return f"Constant(value_type='number')" 
        elif isinstance(node, ast.List) and not node.elts : return "List(elts=[])" # Empty list literal
        elif isinstance(node, ast.BinOp):
            op_map = { ast.Add: "Add", ast.Sub: "Sub", ast.Mult: "Mult", ast.Div: "Div"}
            op_str = op_map.get(type(node.op), type(node.op).__name__)
            left_repr = self._ast_node_to_repr_str(node.left)
            right_repr = self._ast_node_to_repr_str(node.right)
            return f"BinOp({left_repr}, {op_str}, {right_repr})"
        elif isinstance(node, ast.Call):
            func_repr = self._ast_node_to_repr_str(node.func)
            args_repr = [self._ast_node_to_repr_str(arg) for arg in node.args]
            keywords_repr_map = {kw.arg: self._ast_node_to_repr_str(kw.value) for kw in node.keywords}
            return f"Call(func={func_repr}, args=[{', '.join(args_repr)}], keywords={keywords_repr_map})"
        else: return f"UnsupportedASTNode({type(node).__name__})"

    def visit_Assign(self, node, target_operations_list): # Now takes target_operations_list
        current_idx = self.current_op_idx
        if self.is_in_loop_body: current_idx = self.loop_op_idx

        base_operation = { "step_id": self._get_step_id("assign" if not self.is_in_loop_body else "loop_assign") }
        
        # Increment appropriate counter
        if self.is_in_loop_body: self.loop_op_idx += 1
        else: self.current_op_idx += 1


        if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            base_operation["assign_to_variable"] = node.targets[0].id
        else: base_operation["assign_to_variable"] = "_complex_target_"

        if isinstance(node.value, ast.Call):
            call_node = node.value; operation = {**base_operation}; operation["type"] = "function_call"
            if isinstance(call_node.func, ast.Name): operation["target_function_name"] = call_node.func.id
            else: operation["target_function_name"] = "_complex_callable_"
            param_mapping = {}
            for kw in call_node.keywords:
                if isinstance(kw.value, ast.Name): param_mapping[kw.arg] = {"source_type": "variable", "name": kw.value.id}
                elif isinstance(kw.value, ast.Constant): param_mapping[kw.arg] = {"source_type": "constant", "value": kw.value.value}
                else: param_mapping[kw.arg] = {"source_type": "expression_ast", "repr": self._ast_node_to_repr_str(kw.value)}
            operation["parameter_mapping"] = param_mapping
        elif isinstance(node.value, ast.List) and not node.value.elts: # Empty list assignment
            operation = {**base_operation}
            operation["expression_type"] = "list_literal" # New specific type
            operation["expression_ast_repr"] = self._ast_node_to_repr_str(node.value)
        else: 
            operation = {**base_operation}
            operation["expression_type"] = "arithmetic"
            operation["expression_ast_repr"] = self._ast_node_to_repr_str(node.value)
        
        if node.lineno > 0 and (node.lineno -1) < len(self.source_lines):
            assign_line_content = self.source_lines[node.lineno-1]
            comment_idx = assign_line_content.find("#")
            if comment_idx != -1: operation["semantic_purpose"] = assign_line_content[comment_idx+1:].strip()
            else:
                purpose_verb = "Call and assign" if operation.get("type") == "function_call" else "Initialize list" if operation.get("expression_type") == "list_literal" else "Assign value"
                operation["semantic_purpose"] = f"{purpose_verb} to '{operation.get('assign_to_variable', '_unknown_')}'"
        else: operation["semantic_purpose"] = f"Process and assign to '{operation.get('assign_to_variable', '_unknown_')}' (line info unavailable)"
        
        target_operations_list.append(operation)
    
    def visit_Call_Standalone(self, call_node, target_operations_list): # Takes target_operations_list
        current_idx = self.current_op_idx
        if self.is_in_loop_body: current_idx = self.loop_op_idx
        
        operation = {
            "step_id": self._get_step_id("call_expr" if not self.is_in_loop_body else "loop_call_expr"),
            "type": "function_call_standalone", "assign_to_variable": None
        }
        if self.is_in_loop_body: self.loop_op_idx += 1
        else: self.current_op_idx += 1

        if isinstance(call_node.func, ast.Name): operation["target_function_name"] = call_node.func.id
        else: operation["target_function_name"] = "_complex_callable_"
        param_mapping = {}
        for kw in call_node.keywords:
            if isinstance(kw.value, ast.Name): param_mapping[kw.arg] = {"source_type": "variable", "name": kw.value.id}
            elif isinstance(kw.value, ast.Constant): param_mapping[kw.arg] = {"source_type": "constant", "value": kw.value.value}
            else: param_mapping[kw.arg] = {"source_type": "expression_ast", "repr": self._ast_node_to_repr_str(kw.value)}
        operation["parameter_mapping"] = param_mapping
        if call_node.lineno > 0 and (call_node.lineno -1) < len(self.source_lines):
            call_line_content = self.source_lines[call_node.lineno-1]; comment_idx = call_line_content.find("#")
            if comment_idx != -1: operation["semantic_purpose"] = call_line_content[comment_idx+1:].strip()
            else: operation["semantic_purpose"] = f"Execute call to '{operation['target_function_name']}'"
        else: operation["semantic_purpose"] = f"Execute call to '{operation['target_function_name']}' (line info unavailable)"
        target_operations_list.append(operation)

    def visit_For(self, node, target_operations_list): # New method
        # print(f"DEBUG: Visiting For loop, target: {node.target.id if isinstance(node.target, ast.Name) else 'complex'}")
        loop_operation = {
            "step_id": self._get_step_id("loop"), # Main op counter for the loop itself
            "type": "for_loop",
            "target_variable": node.target.id if isinstance(node.target, ast.Name) else "_complex_loop_target_",
            "iterable_source_repr": self._ast_node_to_repr_str(node.iter),
            "loop_body_operations": [] # Nested list for loop body
        }
        self.current_op_idx +=1 # Increment main op counter for the loop op itself

        # Extract inline comment for the 'for' statement itself
        if node.lineno > 0 and (node.lineno - 1) < len(self.source_lines):
            for_line_content = self.source_lines[node.lineno - 1]
            comment_idx = for_line_content.find("#")
            if comment_idx != -1:
                loop_operation["semantic_purpose"] = for_line_content[comment_idx + 1:].strip()
            else:
                loop_operation["semantic_purpose"] = f"Iterate over '{loop_operation['iterable_source_repr']}' with '{loop_operation['target_variable']}'"
        else:
            loop_operation["semantic_purpose"] = f"Iterate (line info unavailable)"
        
        target_operations_list.append(loop_operation)

        # Process the body of the loop. Operations go into the nested list.
        # Temporarily set a flag and a separate counter for loop body operations.
        original_in_loop_flag = self.is_in_loop_body
        self.is_in_loop_body = True
        self.loop_op_idx = 0 # Reset counter for operations *inside* this specific loop
        
        self._process_body_nodes(node.body, current_operations_list=loop_operation["loop_body_operations"])
        
        self.is_in_loop_body = original_in_loop_flag # Restore flag
        # self.loop_op_idx is implicitly reset when another loop starts or visit_For finishes for this instance

    def visit_Return(self, node, source_operations_list): # Now takes source_operations_list
        # Logic to mark the operation that produces the return value
        if node.value and isinstance(node.value, ast.Name):
            self.holoform_data["output_variable_name"] = node.value.id
            for op in reversed(source_operations_list): # Check list it would belong to
                if op.get("assign_to_variable") == node.value.id:
                    op["assign_to_output"] = True
                    current_purpose = op.get("semantic_purpose", "")
                    default_assign_prefix = "Assign value to"; default_call_assign_prefix = "Call and assign to"
                    if current_purpose.startswith(default_assign_prefix) or current_purpose.startswith(default_call_assign_prefix) :
                        op["semantic_purpose"] = f"Set final output '{node.value.id}' from operation: {current_purpose}"
                    break 
        elif node.value:
             self.holoform_data["output_variable_name"] = "_direct_return_expression_"
             return_op = {
                 "step_id": self._get_step_id("return_expr"), "assign_to_output": True,
                 "semantic_purpose": "Return calculated expression directly", "expression_type": "arithmetic",
                 "expression_ast_repr": self._ast_node_to_repr_str(node.value)
             }
             # If return is in a loop, it adds to loop's ops, else to main ops.
             # This logic is now handled by _process_body_nodes passing the correct list
             source_operations_list.append(return_op) 
             if self.is_in_loop_body: self.loop_op_idx +=1 
             else: self.current_op_idx +=1
    
    def get_holoform(self): # Unchanged normalization part
        if self.holoform_data["description"] == "Auto-generated Holoform (default description).":
            op_summary = "its defined interface (no operations parsed)"
            if self.holoform_data["operations"]: op_summary = self.holoform_data['operations'][0].get('semantic_purpose', 'its defined operations')
            self.holoform_data["description"] = f"Function '{self.holoform_data.get('id','unknown_function')}' appears to be for '{op_summary}'."
        if isinstance(self.holoform_data["description"], str):
            cleaned_lines = []; is_comment_block = all(line.lstrip().startswith("#") for line in self.holoform_data["description"].strip().splitlines() if line.strip())
            for line in self.holoform_data["description"].splitlines():
                if is_comment_block: cleaned_lines.append(line.lstrip()[1:].lstrip() if line.lstrip().startswith("#") else line.strip())
                else: cleaned_lines.append(line) 
            if not is_comment_block and cleaned_lines:
                start_idx = 0; end_idx = len(cleaned_lines) -1
                while start_idx < len(cleaned_lines) and not cleaned_lines[start_idx].strip(): start_idx += 1
                while end_idx >= 0 and not cleaned_lines[end_idx].strip(): end_idx -=1
                self.holoform_data["description"] = "\n".join(cleaned_lines[start_idx:end_idx+1])
            else: self.holoform_data["description"] = "\n".join(cleaned_lines).strip()
        return self.holoform_data

def generate_holoform_from_code_string(code_str, function_name_target=None): # Unchanged
    try: parsed_ast = ast.parse(code_str)
    except SyntaxError as e: print(f"ERROR parsing code string: {e}"); return None
    source_lines = code_str.splitlines()
    for node in parsed_ast.body:
        if isinstance(node, ast.FunctionDef):
            if function_name_target is None or node.name == function_name_target:
                visitor = HoloformGeneratorVisitor(source_lines) 
                visitor.visit(node)
                return visitor.get_holoform()
    return None

# --- Main execution for testing ---
if __name__ == "__main__":
    EXPECTED_H_G_HELPER_DOCSTRING_DESC_EXACT = """This is the primary docstring description.
    It has multiple lines.
    And some    leading spaces on this line."""
    EXPECTED_H_G_HELPER_COMMENT_DESC = "Core utility: This is the comment description.\nIt is on the line immediately above the function.\nAnd this comment also has multiple lines."

    test_scenarios = { # Same base scenarios
        "g_helper_with_docstring": { /* ... content as before ... */ },
        "g_helper_with_comment_only": { /* ... content as before ... */ },
        "g_helper_no_desc_defined": { /* ... content as before ... */ }
    }
    # Re-populate base test scenarios for brevity - these are the G_helper ones from previous validated code
    test_scenarios["g_helper_with_docstring"] = {
        "code_str": G_HELPER_GT_CORRECT_CODE_STR_WITH_DOCSTRING, "func_name": "G_helper_gt_correct_docstring",
        "expected_desc": EXPECTED_H_G_HELPER_DOCSTRING_DESC_EXACT,
        "expected_ops_structure_check": [{"assign_to_variable": "result", "expression_ast_repr": "BinOp(BinOp(Name(id='val1'), Mult, Constant(value_type='number')), Add, Name(id='val2'))", "semantic_purpose": "The core calculation for docstring test", "assign_to_output": True}]
    }
    test_scenarios["g_helper_with_comment_only"] = {
        "code_str": G_HELPER_GT_CORRECT_CODE_STR_WITH_COMMENT_ONLY, "func_name": "G_helper_gt_correct_comment",
        "expected_desc": EXPECTED_H_G_HELPER_COMMENT_DESC,
        "expected_ops_structure_check": [{"assign_to_variable": "result", "expression_ast_repr": "BinOp(BinOp(Name(id='val1'), Mult, Constant(value_type='number')), Add, Name(id='val2'))", "semantic_purpose": "The inline comment for operation (comment test)", "assign_to_output": True}]
    }
    test_scenarios["g_helper_no_desc_defined"] = {
        "code_str": G_HELPER_GT_CORRECT_CODE_STR_NO_COMMENT_OR_DOCSTRING, "func_name": "G_helper_gt_correct_no_desc",
        "expected_desc": "Function 'G_helper_gt_correct_no_desc_auto_v1' appears to be for 'The core calculation for no_desc test'.",
        "expected_ops_structure_check": [{"assign_to_variable": "result", "expression_ast_repr": "BinOp(BinOp(Name(id='val1'), Mult, Constant(value_type='number')), Add, Name(id='val2'))", "semantic_purpose": "The core calculation for no_desc test", "assign_to_output": True}]
    }
    test_scenarios["f_caller_with_internal_call"] = { # F_caller test from previous validated code
        "code_str": F_CALLER_GT_CODE_STR, "func_name": "F_caller_gt",
        "expected_desc": "This function demonstrates an internal call.\n    It has pre-call and post-call logic.",
        "expected_ops_structure_check": EXPECTED_F_CALLER_OPERATIONS
    }
    # New test scenario for the loop function
    test_scenarios["f_with_loop"] = {
        "code_str": F_WITH_LOOP_CODE_STR,
        "func_name": "process_items_with_loop",
        "expected_desc": "Processes each item in a list using a factor, accumulating results.",
        "expected_ops_structure_check": EXPECTED_F_WITH_LOOP_OPERATIONS,
        "expected_input_params": ["item_list", "factor"], # Specific checks for this function
        "expected_output_var": "final_result"
    }
    
    all_tests_overall_passed = True
    for scenario_name, details in test_scenarios.items():
        print(f"\n--- Testing Scenario: {scenario_name} ---")
        generated_holoform = generate_holoform_from_code_string(details["code_str"], details["func_name"])
        scenario_passed = True
        if generated_holoform:
            print(f"✔️ Generated Holoform ID: {generated_holoform.get('id')}")
            # For full debug, uncomment next lines:
            # print("GENERATED HOLOFORM:")
            # print(json.dumps(generated_holoform, indent=2))
            # if "expected_ops_structure_check" in details:
            #     print("EXPECTED OPERATIONS STRUCTURE (for validation reference):")
            #     print(json.dumps(details["expected_ops_structure_check"], indent=2))

            gen_desc = generated_holoform["description"]
            exp_desc = details["expected_desc"]
            desc_matches = gen_desc == exp_desc
            print(f"  Description Matches Expected: {'✅ SUCCESS' if desc_matches else '❌ FAILED'}")
            if not desc_matches: scenario_passed = False; all_tests_overall_passed = False; print(f"    Generated: '''{gen_desc}'''\n    Expected:  '''{exp_desc}'''")

            gen_ops = generated_holoform.get("operations", [])
            exp_ops_check = details["expected_ops_structure_check"]
            if len(gen_ops) == len(exp_ops_check):
                for i, gen_op in enumerate(gen_ops):
                    exp_op = exp_ops_check[i]
                    op_match_for_current = True
                    for key, exp_val in exp_op.items():
                        # Special handling for loop_body_operations which is a list of dicts
                        if key == "loop_body_operations" and isinstance(exp_val, list) and isinstance(gen_op.get(key), list):
                            if len(gen_op.get(key)) == len(exp_val):
                                for j, gen_loop_op in enumerate(gen_op.get(key)):
                                    exp_loop_op = exp_val[j]
                                    for l_key, l_exp_val in exp_loop_op.items():
                                        if gen_loop_op.get(l_key) != l_exp_val:
                                            op_match_for_current = False
                                            print(f"    Op[{i}]->LoopOp[{j}] Mismatch on '{l_key}': Gen='{gen_loop_op.get(l_key)}', Exp='{l_exp_val}' ❌")
                                            break
                                    if not op_match_for_current: break
                            else: # Mismatch in number of loop body operations
                                op_match_for_current = False
                                print(f"    Op[{i}] Mismatch on '{key}' (length): Gen#={len(gen_op.get(key))}, Exp#={len(exp_val)} ❌")

                        elif gen_op.get(key) != exp_val : # Regular key-value check
                            op_match_for_current = False
                            print(f"    Op[{i}] Mismatch on '{key}': Gen='{gen_op.get(key)}', Exp='{exp_val}' ❌")
                        
                        if not op_match_for_current: break # Stop checking keys for this op if one failed
                    
                    if not op_match_for_current: scenario_passed = False; all_tests_overall_passed = False
                if scenario_passed and len(gen_ops)>0: print(f"  All Operations Structures Match Expected: ✅ SUCCESS")
            
            else:
                print(f"  Operations Count Mismatch: Gen={len(gen_ops)}, Exp={len(exp_ops_check)} ❌ FAILED")
                # print("Generated Ops:", json.dumps(gen_ops, indent=2)) # Debug
                # print("Expected Ops:", json.dumps(exp_ops_check, indent=2)) # Debug
                scenario_passed = False; all_tests_overall_passed = False
            
            # Params and output name validation based on scenario specifics
            expected_params = details.get("expected_input_params", ["val1", "val2"] if "g_helper" in scenario_name else ["f_input_x"] if "f_caller" in scenario_name else [])
            expected_output_name = details.get("expected_output_var", "result" if "g_helper" in scenario_name else "final_output_f" if "f_caller" in scenario_name else None)

            params_match = generated_holoform.get("input_parameters") == expected_params
            output_match = generated_holoform.get("output_variable_name") == expected_output_name
            if not params_match : print(f"  Input Params Mismatch (Gen: {generated_holoform.get('input_parameters')}, Exp: {expected_params}) ❌ FAILED"); scenario_passed=False; all_tests_overall_passed=False
            if not output_match : print(f"  Output Var Name Mismatch (Gen: {generated_holoform.get('output_variable_name')}, Exp: {expected_output_name}) ❌ FAILED"); scenario_passed=False; all_tests_overall_passed=False
        else:
            print(f"❌ FAILED to generate Holoform for {details['func_name']}.")
            scenario_passed = False; all_tests_overall_passed = False
        print(f"--- Scenario '{scenario_name}' Result: {'PASS' if scenario_passed else 'FAIL'} ---")

    if all_tests_overall_passed:
        print("\n🎉🎉🎉 All Automated Holoform Generation Scenarios (including Loops) Passed!")
    else:
        print("\n⚠️ Some Automated Holoform Generation Scenarios Failed. Please review output.")