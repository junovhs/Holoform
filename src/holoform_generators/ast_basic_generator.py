# AIResearchProject/src/holoform_generators/ast_basic_generator.py
import ast
import json
import inspect 
import re 

# --- Ground Truth Function variations for testing ---
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

# --- Expected Holoform Parts for Validation ---
EXPECTED_H_G_HELPER_DOCSTRING_DESC_EXACT = """This is the primary docstring description.
    It has multiple lines.
    And some    leading spaces on this line."""
EXPECTED_H_G_HELPER_COMMENT_DESC = "# Core utility: This is the comment description.\n# It is on the line immediately above the function.\n# And this comment also has multiple lines."

EXPECTED_F_CALLER_OPERATIONS = [
    {
        "step_id": "s_assign_0",
        "expression_type": "arithmetic",
        "assign_to_variable": "intermediate_val_f",
        "expression_ast_repr": "BinOp(Name(id='f_input_x'), Add, Constant(value_type='number'))",
        "semantic_purpose": "Pre-call logic"
    },
    {
        "step_id": "s_assign_1", # Assuming step_id increments
        "type": "function_call",
        "assign_to_variable": "helper_result_f",
        "target_function_name": "G_helper_gt_correct_docstring",
        "parameter_mapping": {
            "val1": {"source_type": "variable", "name": "f_input_x"},
            "val2": {"source_type": "variable", "name": "intermediate_val_f"}
        },
        "semantic_purpose": "The function call"
    },
    {
        "step_id": "s_assign_2", # Assuming step_id increments
        "expression_type": "arithmetic",
        "assign_to_variable": "final_output_f",
        "expression_ast_repr": "BinOp(Name(id='helper_result_f'), Add, Name(id='f_input_x'))",
        "semantic_purpose": "Post-call logic",
        "assign_to_output": True 
    }
]


# --- AST Node Visitor Class (Revised to handle function calls) ---
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

    def _get_comment_block_above_node(self, node_lineno):
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

    def visit_FunctionDef(self, node):
        self.holoform_data["id"] = f"{node.name}_auto_v1"
        docstring = ast.get_docstring(node, clean=False) 
        if docstring: self.holoform_data["description"] = docstring
        else:
            comments_above = self._get_comment_block_above_node(node.lineno)
            if comments_above: self.holoform_data["description"] = comments_above
        
        for arg in node.args.args: self.holoform_data["input_parameters"].append(arg.arg)
        
        for body_item_idx, body_item in enumerate(node.body):
            if body_item_idx == 0 and isinstance(body_item, ast.Expr) and \
               isinstance(body_item.value, ast.Constant) and \
               isinstance(body_item.value.value, str) and docstring: continue 
            elif isinstance(body_item, ast.Assign): self.visit_Assign(body_item)
            elif isinstance(body_item, ast.Return): self.visit_Return(body_item)
            elif isinstance(body_item, ast.Expr) and isinstance(body_item.value, ast.Call):
                # Handle standalone function call if its result isn't assigned (e.g. a print statement or modifying function)
                self.visit_Call_Standalone(body_item.value) # Need a new method or to adapt visit_Assign/visit_Call logic


    def _ast_node_to_repr_str(self, node):
        if isinstance(node, ast.Name): return f"Name(id='{node.id}')"
        elif isinstance(node, ast.Constant):
            val_type = type(node.value).__name__
            if isinstance(node.value, (int, float)): val_type = 'number' 
            return f"Constant(value_type='{val_type}')" 
        elif isinstance(node, ast.Num): return f"Constant(value_type='number')" 
        elif isinstance(node, ast.BinOp):
            op_map = { ast.Add: "Add", ast.Sub: "Sub", ast.Mult: "Mult", ast.Div: "Div", ast.FloorDiv: "FloorDiv", ast.Mod:"Mod", ast.Pow:"Pow"}
            op_str = op_map.get(type(node.op), type(node.op).__name__)
            left_repr = self._ast_node_to_repr_str(node.left)
            right_repr = self._ast_node_to_repr_str(node.right)
            return f"BinOp({left_repr}, {op_str}, {right_repr})"
        elif isinstance(node, ast.Call): # This helps if a call itself is an argument, not primary use here
            func_repr = self._ast_node_to_repr_str(node.func)
            args_repr = [self._ast_node_to_repr_str(arg) for arg in node.args]
            keywords_repr_map = {kw.arg: self._ast_node_to_repr_str(kw.value) for kw in node.keywords}
            return f"Call(func={func_repr}, args=[{', '.join(args_repr)}], keywords={keywords_repr_map})"
        else: return f"UnsupportedASTNode({type(node).__name__})"

    def visit_Assign(self, node):
        # print(f"DEBUG: visit_Assign, value type: {type(node.value)}")
        base_operation = { "step_id": f"s_assign_{self.current_op_idx}" }
        self.current_op_idx += 1

        if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            base_operation["assign_to_variable"] = node.targets[0].id
        else: base_operation["assign_to_variable"] = "_complex_target_"

        # Check if the value being assigned is a function call
        if isinstance(node.value, ast.Call):
            call_node = node.value
            operation = {**base_operation} # Start with base (step_id, assign_to_variable)
            operation["type"] = "function_call"
            if isinstance(call_node.func, ast.Name): # Direct function call like func()
                operation["target_function_name"] = call_node.func.id
            # elif isinstance(call_node.func, ast.Attribute): # Method call like obj.method()
                # operation["target_function_name"] = f"{self._ast_node_to_repr_str(call_node.func.value)}.{call_node.func.attr}"
            else:
                operation["target_function_name"] = "_complex_callable_"
            
            param_mapping = {}
            # Positional arguments
            # For this POC, we'll assume our target (G_helper) primarily uses keyword args or simple positional that match
            # For F_caller_gt, it uses keywords for G_helper.
            # for i, arg_node in enumerate(call_node.args):
            #     # This needs a way to map positional arg to target Holoform's param name
            #     param_mapping[f"arg{i}"] = {"source_type": "variable", "name": self._ast_node_to_repr_str(arg_node)}

            # Keyword arguments
            for kw in call_node.keywords:
                if isinstance(kw.value, ast.Name): # e.g., val1=some_var
                    param_mapping[kw.arg] = {"source_type": "variable", "name": kw.value.id}
                elif isinstance(kw.value, ast.Constant): # e.g., val1=5
                     param_mapping[kw.arg] = {"source_type": "constant", "value": kw.value.value} # Get actual constant value
                else: # e.g. val1=another_func() or val1=x+y (expression as argument)
                    param_mapping[kw.arg] = {"source_type": "expression_ast", "repr": self._ast_node_to_repr_str(kw.value)}
            operation["parameter_mapping"] = param_mapping
        
        else: # Not a function call, treat as arithmetic/other expression
            operation = {**base_operation}
            operation["expression_type"] = "arithmetic" # Default assumption
            operation["expression_ast_repr"] = self._ast_node_to_repr_str(node.value)
        
        # Extract inline comment for semantic_purpose for either type of operation
        if node.lineno > 0 and (node.lineno -1) < len(self.source_lines):
            assign_line_content = self.source_lines[node.lineno-1]
            comment_idx = assign_line_content.find("#")
            if comment_idx != -1:
                operation["semantic_purpose"] = assign_line_content[comment_idx+1:].strip()
            else:
                purpose_verb = "Call and assign" if operation.get("type") == "function_call" else "Assign value"
                operation["semantic_purpose"] = f"{purpose_verb} to '{operation.get('assign_to_variable', '_unknown_')}'"
        else:
             operation["semantic_purpose"] = f"Process and assign to '{operation.get('assign_to_variable', '_unknown_')}' (line info unavailable)"
        
        self.holoform_data["operations"].append(operation)
    
    # If we need to handle standalone calls like `my_print_func("hello")` that are not assignments:
    def visit_Call_Standalone(self, call_node): # Renamed from visit_Expr in case we need generic visit_Expr later
        # print(f"DEBUG: visit_Call_Standalone, func type: {type(call_node.func)}")
        operation = {
            "step_id": f"s_call_expr_{self.current_op_idx}",
            "type": "function_call_standalone", # Different type
            "assign_to_variable": None # Result not assigned
        }
        self.current_op_idx += 1

        if isinstance(call_node.func, ast.Name): 
            operation["target_function_name"] = call_node.func.id
        else:
            operation["target_function_name"] = "_complex_callable_"
        
        param_mapping = {}
        for kw in call_node.keywords:
            if isinstance(kw.value, ast.Name): 
                param_mapping[kw.arg] = {"source_type": "variable", "name": kw.value.id}
            elif isinstance(kw.value, ast.Constant): 
                 param_mapping[kw.arg] = {"source_type": "constant", "value": kw.value.value}
            else: 
                param_mapping[kw.arg] = {"source_type": "expression_ast", "repr": self._ast_node_to_repr_str(kw.value)}
        operation["parameter_mapping"] = param_mapping
        
        # Extract inline comment for semantic_purpose
        if call_node.lineno > 0 and (call_node.lineno -1) < len(self.source_lines):
            call_line_content = self.source_lines[call_node.lineno-1]
            comment_idx = call_line_content.find("#")
            if comment_idx != -1:
                operation["semantic_purpose"] = call_line_content[comment_idx+1:].strip()
            else:
                operation["semantic_purpose"] = f"Execute call to '{operation['target_function_name']}'"
        else:
             operation["semantic_purpose"] = f"Execute call to '{operation['target_function_name']}' (line info unavailable)"
        
        self.holoform_data["operations"].append(operation)


    def visit_Return(self, node):
        if node.value and isinstance(node.value, ast.Name):
            self.holoform_data["output_variable_name"] = node.value.id
            for op in reversed(self.holoform_data["operations"]):
                if op.get("assign_to_variable") == node.value.id:
                    op["assign_to_output"] = True
                    current_purpose = op.get("semantic_purpose", "")
                    base_purpose = current_purpose
                    # Check if it's a default message from an assignment we can make more specific for output
                    default_assign_prefix = "Assign value to" 
                    default_call_assign_prefix = "Call and assign to"
                    if current_purpose.startswith(default_assign_prefix) or current_purpose.startswith(default_call_assign_prefix) :
                        op["semantic_purpose"] = f"Set final output '{node.value.id}' from operation: {base_purpose}"
                    # Otherwise, keep the specific purpose from inline comment or specific call info
                    break 
        elif node.value: # Direct return of an expression
             self.holoform_data["output_variable_name"] = "_direct_return_expression_"
             return_op = {
                 "step_id": f"s_return_expr_{self.current_op_idx}", "assign_to_output": True,
                 "semantic_purpose": "Return calculated expression directly", "expression_type": "arithmetic", # Or "expression"
                 "expression_ast_repr": self._ast_node_to_repr_str(node.value)
             }
             self.holoform_data["operations"].append(return_op)
             self.current_op_idx += 1
    
    def get_holoform(self):
        if self.holoform_data["description"] == "Auto-generated Holoform (default description).":
            op_summary = "its defined interface (no operations parsed)"
            if self.holoform_data["operations"]:
                op_summary = self.holoform_data['operations'][0].get('semantic_purpose', 'its defined operations')
            self.holoform_data["description"] = f"Function '{self.holoform_data.get('id','unknown_function')}' appears to be for '{op_summary}'."
        if isinstance(self.holoform_data["description"], str):
            cleaned_lines = []
            is_comment_block = all(line.lstrip().startswith("#") for line in self.holoform_data["description"].strip().splitlines() if line.strip())
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

def generate_holoform_from_code_string(code_str, function_name_target=None):
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

    base_test_scenarios = { # G_helper tests from before
        "g_helper_with_docstring": {
            "code_str": G_HELPER_GT_CORRECT_CODE_STR_WITH_DOCSTRING,
            "func_name": "G_helper_gt_correct_docstring",
            "expected_desc": EXPECTED_H_G_HELPER_DOCSTRING_DESC_EXACT,
            "expected_ops_structure_check": [ # Just check key fields, not all
                {"assign_to_variable": "result", "expression_ast_repr": "BinOp(BinOp(Name(id='val1'), Mult, Constant(value_type='number')), Add, Name(id='val2'))", "semantic_purpose": "The core calculation for docstring test", "assign_to_output": True}
            ]
        },
        "g_helper_with_comment_only": {
            "code_str": G_HELPER_GT_CORRECT_CODE_STR_WITH_COMMENT_ONLY,
            "func_name": "G_helper_gt_correct_comment",
            "expected_desc": EXPECTED_H_G_HELPER_COMMENT_DESC,
            "expected_ops_structure_check": [
                {"assign_to_variable": "result", "expression_ast_repr": "BinOp(BinOp(Name(id='val1'), Mult, Constant(value_type='number')), Add, Name(id='val2'))", "semantic_purpose": "The inline comment for operation (comment test)", "assign_to_output": True}
            ]
        },
         "g_helper_no_desc_defined": {
            "code_str": G_HELPER_GT_CORRECT_CODE_STR_NO_COMMENT_OR_DOCSTRING,
            "func_name": "G_helper_gt_correct_no_desc",
            "expected_desc": "Function 'G_helper_gt_correct_no_desc_auto_v1' appears to be for 'The core calculation for no_desc test'.",
            "expected_ops_structure_check": [
                {"assign_to_variable": "result", "expression_ast_repr": "BinOp(BinOp(Name(id='val1'), Mult, Constant(value_type='number')), Add, Name(id='val2'))", "semantic_purpose": "The core calculation for no_desc test", "assign_to_output": True}
            ]
        }
    }

    f_caller_test_scenario = {
        "f_caller_with_internal_call": {
            "code_str": F_CALLER_GT_CODE_STR,
            "func_name": "F_caller_gt",
            "expected_desc": "This function demonstrates an internal call.\n    It has pre-call and post-call logic.",
            "expected_ops_structure_check": EXPECTED_F_CALLER_OPERATIONS # Use the detailed expected ops
        }
    }
    
    all_tests_overall_passed = True

    # Combine all scenarios
    test_scenarios_combined = {**base_test_scenarios, **f_caller_test_scenario}

    for scenario_name, details in test_scenarios_combined.items():
        print(f"\n--- Testing Scenario: {scenario_name} ---")
        generated_holoform = generate_holoform_from_code_string(details["code_str"], details["func_name"])
        scenario_passed = True
        if generated_holoform:
            print(f"✔️ Generated Holoform ID: {generated_holoform.get('id')}")
            # To print the full generated holoform for debugging:
            # print("GENERATED:")
            # print(json.dumps(generated_holoform, indent=2))
            # print("EXPECTED OPS (for f_caller scenario for comparison):")
            # if scenario_name == "f_caller_with_internal_call":
            #     print(json.dumps(EXPECTED_F_CALLER_OPERATIONS, indent=2))


            gen_desc = generated_holoform["description"]
            exp_desc = details["expected_desc"]
            desc_matches = gen_desc == exp_desc
            print(f"  Description Matches Expected: {'✅ SUCCESS' if desc_matches else '❌ FAILED'}")
            if not desc_matches: scenario_passed = False; all_tests_overall_passed = False; print(f"    Generated: '''{gen_desc}'''\n    Expected:  '''{exp_desc}'''")

            # Validate Operations more carefully for F_caller
            gen_ops = generated_holoform.get("operations", [])
            exp_ops_check = details["expected_ops_structure_check"]
            
            if len(gen_ops) == len(exp_ops_check):
                for i, gen_op in enumerate(gen_ops):
                    exp_op = exp_ops_check[i]
                    op_match = True
                    for key, exp_val in exp_op.items():
                        if gen_op.get(key) != exp_val:
                            op_match = False
                            print(f"    Op[{i}] Mismatch on '{key}': Gen='{gen_op.get(key)}', Exp='{exp_val}' ❌")
                            break
                    if not op_match: scenario_passed = False; all_tests_overall_passed = False
                if scenario_passed : print(f"  All Operations Structures Match Expected: ✅ SUCCESS")

            else:
                print(f"  Operations Count Mismatch: Gen={len(gen_ops)}, Exp={len(exp_ops_check)} ❌ FAILED")
                scenario_passed = False; all_tests_overall_passed = False
            
            # Params and output name validation common for all G_helper variants
            if "g_helper" in scenario_name:
                params_match = generated_holoform.get("input_parameters") == ["val1", "val2"]
                output_match = generated_holoform.get("output_variable_name") == "result"
            elif scenario_name == "f_caller_with_internal_call":
                params_match = generated_holoform.get("input_parameters") == ["f_input_x"]
                output_match = generated_holoform.get("output_variable_name") == "final_output_f"

            if not params_match : print(f"  Input Params Mismatch ❌ FAILED"); scenario_passed=False; all_tests_overall_passed=False
            if not output_match : print(f"  Output Var Name Mismatch ❌ FAILED"); scenario_passed=False; all_tests_overall_passed=False
        else:
            print(f"❌ FAILED to generate Holoform for {details['func_name']}.")
            scenario_passed = False; all_tests_overall_passed = False
        print(f"--- Scenario '{scenario_name}' Result: {'PASS' if scenario_passed else 'FAIL'} ---")

    if all_tests_overall_passed:
        print("\n🎉🎉🎉 All Automated Holoform Generation Scenarios (including F_caller) Passed!")
    else:
        print("\n⚠️ Some Automated Holoform Generation Scenarios Failed. Please review output.")