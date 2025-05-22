# AIResearchProject/src/holoform_generators/ast_basic_generator.py
import ast
import json
import inspect # For getting source lines more reliably
import re # For string substitution (normalizing whitespace)

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


# --- Target Holoform Structure (what we aim to generate for specific cases) ---
# These are used for validation in the __main__ block.
EXPECTED_H_G_HELPER_DOCSTRING_DESC = "This is the primary docstring description.\n  It has multiple lines.\n  And some    leading spaces on this line."
EXPECTED_H_G_HELPER_COMMENT_DESC = "# Core utility: This is the comment description.\n# It is on the line immediately above the function.\n# And this comment also has multiple lines."


# --- AST Node Visitor Class (Revised for better description handling) ---
class HoloformGeneratorVisitor(ast.NodeVisitor):
    def __init__(self, source_code_lines_list):
        self.source_lines = source_code_lines_list
        self.holoform_data = {
            "id": "",
            "parent_module_id": "Unknown_Module_AST_v1", 
            "description": "Auto-generated Holoform (default description).",
            "tags": ["ast_generated"],
            "input_parameters": [],
            "operations": [],
            "output_variable_name": None
        }
        self.current_op_idx = 0

    def _get_comment_block_above_node(self, node_lineno):
        if node_lineno <= 1:
            return None
        comment_block_lines = []
        current_line_idx = node_lineno - 2 
        while current_line_idx >= 0:
            line_content = self.source_lines[current_line_idx].strip() # Strip individual lines here for checker
            original_line_content = self.source_lines[current_line_idx] # Keep original for holoform
            if line_content.startswith("#"):
                comment_block_lines.insert(0, original_line_content) 
            elif not line_content: 
                if comment_block_lines: break 
            else: break
            current_line_idx -= 1
        return "\n".join(comment_block_lines) if comment_block_lines else None

    def visit_FunctionDef(self, node):
        self.holoform_data["id"] = f"{node.name}_auto_v1"
        docstring = ast.get_docstring(node, clean=False) 
        if docstring:
            self.holoform_data["description"] = docstring
        else:
            comments_above = self._get_comment_block_above_node(node.lineno)
            if comments_above:
                self.holoform_data["description"] = comments_above
        
        for arg in node.args.args:
            self.holoform_data["input_parameters"].append(arg.arg)
        
        for body_item_idx, body_item in enumerate(node.body):
            if body_item_idx == 0 and isinstance(body_item, ast.Expr) and \
               isinstance(body_item.value, ast.Constant) and \
               isinstance(body_item.value.value, str) and docstring:
                continue 
            elif isinstance(body_item, ast.Assign):
                self.visit_Assign(body_item)
            elif isinstance(body_item, ast.Return):
                self.visit_Return(body_item)

    def _ast_node_to_repr_str(self, node):
        if isinstance(node, ast.Name): return f"Name(id='{node.id}')"
        elif isinstance(node, ast.Constant):
            val_type = type(node.value).__name__
            # For testing consistency, we want to know if it's a number, but not the exact number
            if isinstance(node.value, (int, float)): val_type = 'number' 
            return f"Constant(value_type='{val_type}')" 
        elif isinstance(node, ast.Num): return f"Constant(value_type='number')" 
        elif isinstance(node, ast.BinOp):
            op_map = { ast.Add: "Add", ast.Sub: "Sub", ast.Mult: "Mult", ast.Div: "Div", ast.FloorDiv: "FloorDiv", ast.Mod:"Mod", ast.Pow:"Pow"}
            op_str = op_map.get(type(node.op), type(node.op).__name__)
            left_repr = self._ast_node_to_repr_str(node.left)
            right_repr = self._ast_node_to_repr_str(node.right)
            return f"BinOp({left_repr}, {op_str}, {right_repr})"
        elif isinstance(node, ast.Call):
            func_repr = self._ast_node_to_repr_str(node.func)
            args_repr = [self._ast_node_to_repr_str(arg) for arg in node.args]
            return f"Call(func={func_repr}, args=[{', '.join(args_repr)}])"
        else: return f"UnsupportedASTNode({type(node).__name__})"

    def visit_Assign(self, node):
        operation = {
            "step_id": f"s_assign_{self.current_op_idx}",
            "expression_type": "arithmetic" 
        }
        self.current_op_idx += 1
        if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            operation["assign_to_variable"] = node.targets[0].id
        else: operation["assign_to_variable"] = "_complex_target_"
        operation["expression_ast_repr"] = self._ast_node_to_repr_str(node.value)
        
        if node.lineno > 0 and (node.lineno -1) < len(self.source_lines):
            assign_line_content = self.source_lines[node.lineno-1]
            comment_idx = assign_line_content.find("#")
            if comment_idx != -1:
                operation["semantic_purpose"] = assign_line_content[comment_idx+1:].strip()
            else:
                operation["semantic_purpose"] = f"Assign value to '{operation['assign_to_variable']}'"
        else:
             operation["semantic_purpose"] = f"Assign value to '{operation['assign_to_variable']}' (line info unavailable)"
        self.holoform_data["operations"].append(operation)

    def visit_Return(self, node):
        if node.value and isinstance(node.value, ast.Name):
            self.holoform_data["output_variable_name"] = node.value.id
            for op in reversed(self.holoform_data["operations"]):
                if op.get("assign_to_variable") == node.value.id:
                    op["assign_to_output"] = True
                    current_purpose = op.get("semantic_purpose", "")
                    if current_purpose.startswith("Assign value to"): 
                        op["semantic_purpose"] = f"Set final output '{node.value.id}' from prior assignment"
                    break 
        elif node.value:
             self.holoform_data["output_variable_name"] = "_direct_return_expression_"
             return_op = {
                 "step_id": f"s_return_expr_{self.current_op_idx}", "assign_to_output": True,
                 "semantic_purpose": "Return calculated expression directly", "expression_type": "arithmetic",
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
            # Process lines to handle comment markers and preserve intentional docstring indentation
            is_comment_block = all(line.lstrip().startswith("#") for line in self.holoform_data["description"].strip().splitlines() if line.strip())

            for line in self.holoform_data["description"].splitlines():
                if is_comment_block:
                    cleaned_lines.append(line.lstrip()[1:].lstrip() if line.lstrip().startswith("#") else line.strip())
                else: # Docstring, preserve relative indentation by only stripping fully blank lines at start/end
                    cleaned_lines.append(line) 
            
            # Smartly join docstring lines (handle leading/trailing empty lines from split)
            if not is_comment_block and cleaned_lines:
                start_idx = 0
                while start_idx < len(cleaned_lines) and not cleaned_lines[start_idx].strip():
                    start_idx += 1
                end_idx = len(cleaned_lines) -1
                while end_idx >= 0 and not cleaned_lines[end_idx].strip():
                    end_idx -=1
                self.holoform_data["description"] = "\n".join(cleaned_lines[start_idx:end_idx+1])

            else: # Comment block or single line
                 self.holoform_data["description"] = "\n".join(cleaned_lines).strip()


        return self.holoform_data

def generate_holoform_from_code_string(code_str, function_name_target=None):
    try:
        parsed_ast = ast.parse(code_str)
    except SyntaxError as e:
        print(f"ERROR parsing code string: {e}")
        return None
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
    # Updated EXPECTED_H_G_HELPER_DOCSTRING_DESC to match exact multiline docstring format
    EXPECTED_H_G_HELPER_DOCSTRING_DESC_EXACT = """This is the primary docstring description.
    It has multiple lines.
    And some    leading spaces on this line."""


    test_scenarios = {
        "with_docstring": {
            "code_str": G_HELPER_GT_CORRECT_CODE_STR_WITH_DOCSTRING,
            "func_name": "G_helper_gt_correct_docstring",
            "expected_desc": EXPECTED_H_G_HELPER_DOCSTRING_DESC_EXACT,
            "expected_op_sem_purp": "The core calculation for docstring test",
            "expected_ast_repr": "BinOp(BinOp(Name(id='val1'), Mult, Constant(value_type='number')), Add, Name(id='val2'))"
        },
        "with_comment_only": {
            "code_str": G_HELPER_GT_CORRECT_CODE_STR_WITH_COMMENT_ONLY,
            "func_name": "G_helper_gt_correct_comment",
            "expected_desc": "Core utility: This is the comment description.\nIt is on the line immediately above the function.\nAnd this comment also has multiple lines.",
            "expected_op_sem_purp": "The inline comment for operation (comment test)",
            "expected_ast_repr": "BinOp(BinOp(Name(id='val1'), Mult, Constant(value_type='number')), Add, Name(id='val2'))"
        },
        "no_desc_defined": {
            "code_str": G_HELPER_GT_CORRECT_CODE_STR_NO_COMMENT_OR_DOCSTRING,
            "func_name": "G_helper_gt_correct_no_desc",
            "expected_desc": "Function 'G_helper_gt_correct_no_desc_auto_v1' appears to be for 'The core calculation for no_desc test'.",
            "expected_op_sem_purp": "The core calculation for no_desc test",
            "expected_ast_repr": "BinOp(BinOp(Name(id='val1'), Mult, Constant(value_type='number')), Add, Name(id='val2'))"
        }
    }

    all_tests_overall_passed = True
    for scenario_name, details in test_scenarios.items():
        print(f"\n--- Testing Scenario: {scenario_name} ---")
        generated_holoform = generate_holoform_from_code_string(details["code_str"], details["func_name"])
        
        scenario_passed = True
        if generated_holoform:
            print(f"✔️ Generated Holoform ID: {generated_holoform.get('id')}")
            # print(json.dumps(generated_holoform, indent=2)) # For debugging generated structure
            
            # Validate Description
            gen_desc = generated_holoform["description"]
            exp_desc = details["expected_desc"]
            desc_matches = gen_desc == exp_desc
            
            print(f"  Description Matches Expected: {'✅ SUCCESS' if desc_matches else '❌ FAILED'}")
            if not desc_matches:
                scenario_passed = False; all_tests_overall_passed = False
                print(f"    Generated: '''{gen_desc}'''")
                print(f"    Expected:  '''{exp_desc}'''")

            # Validate Operations 
            if len(generated_holoform.get("operations", [])) == 1:
                gen_op = generated_holoform["operations"][0]
                
                ast_repr_matches = gen_op.get("expression_ast_repr") == details["expected_ast_repr"]
                print(f"  Operation 'expression_ast_repr' Matches: {'✅ SUCCESS' if ast_repr_matches else '❌ FAILED'}")
                if not ast_repr_matches: scenario_passed = False; all_tests_overall_passed = False; print(f"    Gen AST Repr: {gen_op.get('expression_ast_repr')}\n    Exp AST Repr: {details['expected_ast_repr']}")
                
                sem_purp_matches = gen_op.get("semantic_purpose") == details["expected_op_sem_purp"]
                print(f"  Operation 'semantic_purpose' Matches: {'✅ SUCCESS' if sem_purp_matches else '❌ FAILED'}")
                if not sem_purp_matches: scenario_passed = False; all_tests_overall_passed = False; print(f"    Gen SemPurp: '{gen_op.get('semantic_purpose')}'\n    Exp SemPurp: '{details['expected_op_sem_purp']}'")
                
                output_assignment_ok = ("assign_to_output" in gen_op and gen_op.get("assign_to_output") == True)
                if not output_assignment_ok :
                    print(f"  Operation 'assign_to_output' Flag Check: {'✅ SUCCESS' if output_assignment_ok else '❌ FAILED (flag not set or false)'}")
                    scenario_passed=False; all_tests_overall_passed=False
            else:
                print(f"  Operations Count Mismatch (expected 1): {len(generated_holoform.get('operations', []))} ❌ FAILED")
                scenario_passed = False; all_tests_overall_passed = False
            
            expected_params = ["val1", "val2"]
            expected_output_name = "result"
            params_match = generated_holoform.get("input_parameters") == expected_params
            output_match = generated_holoform.get("output_variable_name") == expected_output_name
            if not params_match : print(f"  Input Params Mismatch ❌ FAILED"); scenario_passed=False; all_tests_overall_passed=False
            if not output_match : print(f"  Output Var Name Mismatch ❌ FAILED"); scenario_passed=False; all_tests_overall_passed=False

        else:
            print(f"❌ FAILED to generate Holoform for {details['func_name']}.")
            scenario_passed = False; all_tests_overall_passed = False
        print(f"--- Scenario '{scenario_name}' Result: {'PASS' if scenario_passed else 'FAIL'} ---")

    if all_tests_overall_passed:
        print("\n🎉🎉🎉 All Automated Holoform Generation Scenarios Passed for Description & Core Ops!")
    else:
        print("\n⚠️ Some Automated Holoform Generation Scenarios Failed. Please review output.")
