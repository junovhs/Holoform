# AIResearchProject/src/holoform_generators/ast_basic_generator.py
import ast
import json

# --- Ground Truth Function (as a string for parsing) ---
G_HELPER_GT_CORRECT_CODE_STR = """
def G_helper_gt_correct(val1, val2):
    # Core utility: Multiplies val1 by 2 and adds val2.
    result = (val1 * 2) + val2 # The core calculation
    return result
"""

# --- Target Holoform Structure (what we aim to generate) ---
EXPECTED_H_G_HELPER = {
    "id": "G_helper_v1_auto", 
    "parent_module_id": "Unknown_Module_AST_v1", 
    "description": "Core utility: Multiplies val1 by 2 and adds val2.", 
    "tags": ["core_utility", "arithmetic_worker", "ast_generated"], 
    "input_parameters": ["val1", "val2"], 
    "operations": [
        {
            "assign_to_variable": "result", 
            "expression_type": "arithmetic", 
            "expression_ast_repr": "BinOp(BinOp(Name(id='val1'), Mult, Num(n=2)), Add, Name(id='val2'))", 
            "semantic_purpose": "Perform core G_helper calculation"
        }
    ],
    "output_variable_name": "result"
}

# --- AST Node Visitor Class ---
class HoloformGeneratorVisitor(ast.NodeVisitor):
    def __init__(self, source_code_str):
        self.source_lines = source_code_str.splitlines()
        self.holoform_data = {
            "id": "",
            "parent_module_id": "Unknown_Module_AST_v1", # Default
            "description": "Auto-generated Holoform.", # Default
            "tags": ["ast_generated"],
            "input_parameters": [],
            "operations": [],
            "output_variable_name": None
        }
        self.current_op_idx = 0

    def _get_function_comment(self, node):
        """Simplified: attempts to get a comment directly above the function."""
        if node.lineno > 1:
            comment_line_idx = node.lineno - 2 # 0-indexed line number
            if comment_line_idx >= 0 and comment_line_idx < len(self.source_lines):
                potential_comment = self.source_lines[comment_line_idx].strip()
                if potential_comment.startswith("#"):
                    return potential_comment[1:].strip()
        return None # No suitable comment found immediately above

    def visit_FunctionDef(self, node):
        # print(f"DEBUG: Visiting FunctionDef: {node.name}")
        self.holoform_data["id"] = f"{node.name}_auto_v1"
        
        docstring = ast.get_docstring(node)
        if docstring:
            self.holoform_data["description"] = docstring.strip()
        else:
            comment_above = self._get_function_comment(node)
            if comment_above:
                self.holoform_data["description"] = comment_above
            # else it keeps the default "Auto-generated Holoform."

        for arg in node.args.args:
            self.holoform_data["input_parameters"].append(arg.arg)
        
        # Only process body items directly, not using generic_visit for this simple case
        for body_item in node.body:
            if isinstance(body_item, ast.Assign):
                self.visit_Assign(body_item)
            elif isinstance(body_item, ast.Return):
                self.visit_Return(body_item)
            elif isinstance(body_item, ast.Expr) and isinstance(body_item.value, ast.Constant) and isinstance(body_item.value.value, str):
                pass # This is likely the docstring we've already processed
            else:
                print(f"  WARNING: AST Generator skipping unhandled body item type in FunctionDef: {type(body_item)}")


    def _ast_node_to_repr_str(self, node):
        if isinstance(node, ast.Name):
            return f"Name(id='{node.id}')"
        elif isinstance(node, ast.Constant): # Python 3.8+ for numbers, strings etc.
            if isinstance(node.value, (int, float)):
                return f"Num(n={node.value})"
            elif isinstance(node.value, str):
                return f"Str(s='{node.value}')" # Should not happen in G_helper expression
            else:
                return f"Constant(value_type='{type(node.value).__name__}')"
        elif isinstance(node, ast.Num): # For older Python (deprecated in 3.8)
            return f"Num(n={node.n})"
        elif isinstance(node, ast.BinOp):
            op_map = { ast.Add: "Add", ast.Sub: "Sub", ast.Mult: "Mult", ast.Div: "Div", ast.FloorDiv: "FloorDiv", ast.Mod: "Mod", ast.Pow: "Pow" }
            op_str = op_map.get(type(node.op), type(node.op).__name__)
            left_repr = self._ast_node_to_repr_str(node.left)
            right_repr = self._ast_node_to_repr_str(node.right)
            return f"BinOp({left_repr}, {op_str}, {right_repr})"
        elif isinstance(node, ast.Call):
            func_repr = self._ast_node_to_repr_str(node.func)
            args_repr = [self._ast_node_to_repr_str(arg) for arg in node.args]
            # keywords_repr not handled here for simplicity
            return f"Call(func={func_repr}, args=[{', '.join(args_repr)}])"
        else:
            return f"UnsupportedASTNode({type(node).__name__})"

    def visit_Assign(self, node):
        # print(f"DEBUG:   Visiting Assign: target(s) {[t.id for t in node.targets if isinstance(t, ast.Name)]}")
        operation = {
            "step_id": f"s_assign_{self.current_op_idx}",
            "semantic_purpose": "Assign value", # Default, could be improved
            "expression_type": "arithmetic" 
        }
        self.current_op_idx += 1

        if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            operation["assign_to_variable"] = node.targets[0].id
        else:
            operation["assign_to_variable"] = "_complex_target_" 

        operation["expression_ast_repr"] = self._ast_node_to_repr_str(node.value)
        
        # Attempt to extract comment for this assignment as semantic_purpose
        if node.lineno > 0 and node.lineno <= len(self.source_lines):
            assign_line_content = self.source_lines[node.lineno-1]
            comment_idx = assign_line_content.find("#")
            if comment_idx != -1:
                operation["semantic_purpose"] = assign_line_content[comment_idx+1:].strip()

        self.holoform_data["operations"].append(operation)

    def visit_Return(self, node):
        # print(f"DEBUG:   Visiting Return")
        if node.value and isinstance(node.value, ast.Name):
            self.holoform_data["output_variable_name"] = node.value.id
            # Mark the operation that assigned to this variable as the outputting operation
            for op in reversed(self.holoform_data["operations"]): # Check recent ops
                if op.get("assign_to_variable") == node.value.id:
                    op["assign_to_output"] = True
                    # We could update semantic_purpose, but it's tricky to know which comment belongs if multi-line
                    break 
        elif node.value: # Direct return of an expression
             self.holoform_data["output_variable_name"] = "_direct_return_expression_"
             return_op = {
                 "step_id": f"s_return_expr_{self.current_op_idx}",
                 "assign_to_output": True,
                 "semantic_purpose": "Return calculated expression",
                 "expression_type": "arithmetic",
                 "expression_ast_repr": self._ast_node_to_repr_str(node.value)
             }
             self.holoform_data["operations"].append(return_op)
             self.current_op_idx += 1
        # else: no return value, e.g. "return"

    def get_holoform(self):
        # Post-processing: if a description wasn't found via comment/docstring
        if self.holoform_data["description"] == "Auto-generated Holoform." and self.holoform_data["operations"]:
             self.holoform_data["description"] = f"Auto-generated Holoform for function {self.holoform_data['id']}. Primary action: {self.holoform_data['operations'][0]['semantic_purpose']}"

        return self.holoform_data

def generate_holoform_from_code_string(code_str, function_name_target=None):
    parsed_ast = ast.parse(code_str)
    for node in parsed_ast.body:
        if isinstance(node, ast.FunctionDef):
            if function_name_target is None or node.name == function_name_target:
                # print(f"\nDEBUG: Processing function: {node.name} for Holoform generation...")
                visitor = HoloformGeneratorVisitor(code_str) # Pass full code for comment context
                visitor.visit(node)
                return visitor.get_holoform()
    return None

# --- Main execution for testing ---
if __name__ == "__main__":
    print("--- Automated Holoform Generation POC v1 (G_helper_gt_correct) ---")
    
    generated_g_helper_holoform = generate_holoform_from_code_string(G_HELPER_GT_CORRECT_CODE_STR, "G_helper_gt_correct")
    
    if generated_g_helper_holoform:
        print("\n✔️ SUCCESSFULLY GENERATED HOLOFORM:")
        print(json.dumps(generated_g_helper_holoform, indent=4))

        print("\n🔍 EXPECTED HOLOFORM STRUCTURE (for comparison):")
        print(json.dumps(EXPECTED_H_G_HELPER, indent=4))

        # Basic Validation
        print("\n--- Basic Validation Against Expected ---")
        valid_params = generated_g_helper_holoform["input_parameters"] == EXPECTED_H_G_HELPER["input_parameters"]
        print(f"Input Parameters Match Expected: {'✅ SUCCESS' if valid_params else '❌ FAILED'}")

        valid_output_var = generated_g_helper_holoform["output_variable_name"] == EXPECTED_H_G_HELPER["output_variable_name"]
        print(f"Output Variable Name Matches Expected: {'✅ SUCCESS' if valid_output_var else '❌ FAILED'}")
        
        valid_desc = generated_g_helper_holoform["description"] == EXPECTED_H_G_HELPER["description"]
        print(f"Description Matches Expected (from comment): {'✅ SUCCESS' if valid_desc else '❌ FAILED'}")
        if not valid_desc:
            print(f"  Generated Desc: '{generated_g_helper_holoform['description']}'")
            print(f"  Expected Desc:  '{EXPECTED_H_G_HELPER['description']}'")

        # Operation structure validation
        if len(generated_g_helper_holoform["operations"]) == 1 and len(EXPECTED_H_G_HELPER["operations"]) == 1:
            gen_op = generated_g_helper_holoform["operations"][0]
            exp_op = EXPECTED_H_G_HELPER["operations"][0]
            valid_op_assign = gen_op.get("assign_to_variable") == exp_op.get("assign_to_variable")
            print(f"Operation 'assign_to_variable' Matches: {'✅ SUCCESS' if valid_op_assign else '❌ FAILED'}")
            
            valid_op_expr_repr = gen_op.get("expression_ast_repr") == exp_op.get("expression_ast_repr")
            print(f"Operation 'expression_ast_repr' Matches: {'✅ SUCCESS' if valid_op_expr_repr else '❌ FAILED'}")
            if not valid_op_expr_repr:
                print(f"  Generated AST Repr: {gen_op.get('expression_ast_repr')}")
                print(f"  Expected AST Repr:  {exp_op.get('expression_ast_repr')}")

            valid_op_sem_purp = gen_op.get("semantic_purpose") == exp_op.get("semantic_purpose") # Comparing against refined expected value
            exp_op_sem_purp_check = "Perform core G_helper calculation" # Simplified check
            if gen_op.get("semantic_purpose") == exp_op_sem_purp_check : valid_op_sem_purp = True
            print(f"Operation 'semantic_purpose' Matches (from inline comment): {'✅ SUCCESS' if valid_op_sem_purp else '❌ FAILED'}")
            if not valid_op_sem_purp:
                 print(f"  Generated SemPurp: '{gen_op.get('semantic_purpose')}'")
                 print(f"  Expected SemPurp:  '{exp_op_sem_purp_check}' (or similar)")

        else:
            print("Operation Count Mismatch: ❌ FAILED")
    else:
        print("\n❌ FAILED to generate Holoform for G_helper_gt_correct.")