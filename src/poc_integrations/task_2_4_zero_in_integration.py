import ast
import json
import re 
import os 

# --- Content from: constants.py ---
DEFAULT_PARENT_MODULE_ID = "Unknown_Module_AST_v1"
DEFAULT_DESCRIPTION = "Auto-generated Holoform (default description)."
DEFAULT_TAGS = ["ast_generated"]
UNSUPPORTED_NODE_PREFIX = "UnsupportedASTNode"
KEY_ID = "id"
KEY_PARENT_MODULE_ID = "parent_module_id"
KEY_DESCRIPTION = "description"
KEY_TAGS = "tags"
KEY_INPUT_PARAMETERS = "input_parameters"
KEY_OPERATIONS = "operations"
KEY_OUTPUT_VARIABLE_NAME = "output_variable_name"
KEY_INTERNAL_VARIABLES = "internal_variables_config"
KEY_OP_STEP_ID = "step_id"
KEY_OP_TYPE = "type"
KEY_OP_EXPRESSION_TYPE = "expression_type"
KEY_OP_SEMANTIC_PURPOSE = "semantic_purpose"
KEY_OP_ASSIGN_TO_VARIABLE = "assign_to_variable"
KEY_OP_EXPRESSION_AST_REPR = "expression_ast_repr"
KEY_OP_ASSIGN_TO_OUTPUT = "assign_to_output"
KEY_OP_TARGET_FUNCTION_NAME = "target_function_name"
KEY_OP_PARAMETER_MAPPING = "parameter_mapping"
KEY_OP_LOOP_TARGET_VARIABLE = "target_variable"
KEY_OP_LOOP_ITERABLE_REPR = "iterable_source_repr"
KEY_OP_LOOP_BODY_OPERATIONS = "loop_body_operations"

class ConstantsAlias: pass
C = ConstantsAlias()
C.DEFAULT_PARENT_MODULE_ID = DEFAULT_PARENT_MODULE_ID
C.DEFAULT_DESCRIPTION = DEFAULT_DESCRIPTION
C.DEFAULT_TAGS = DEFAULT_TAGS
C.KEY_ID = KEY_ID
C.KEY_PARENT_MODULE_ID = KEY_PARENT_MODULE_ID
C.KEY_DESCRIPTION = KEY_DESCRIPTION
C.KEY_TAGS = KEY_TAGS
C.KEY_INPUT_PARAMETERS = KEY_INPUT_PARAMETERS
C.KEY_OPERATIONS = KEY_OPERATIONS
C.KEY_OUTPUT_VARIABLE_NAME = KEY_OUTPUT_VARIABLE_NAME
C.KEY_OP_STEP_ID = KEY_OP_STEP_ID
C.KEY_OP_TYPE = KEY_OP_TYPE
C.KEY_OP_ASSIGN_TO_VARIABLE = KEY_OP_ASSIGN_TO_VARIABLE
C.KEY_OP_EXPRESSION_TYPE = KEY_OP_EXPRESSION_TYPE
C.KEY_OP_EXPRESSION_AST_REPR = KEY_OP_EXPRESSION_AST_REPR
C.KEY_OP_SEMANTIC_PURPOSE = KEY_OP_SEMANTIC_PURPOSE
C.KEY_OP_TARGET_FUNCTION_NAME = KEY_OP_TARGET_FUNCTION_NAME
C.KEY_OP_PARAMETER_MAPPING = KEY_OP_PARAMETER_MAPPING
C.KEY_OP_LOOP_TARGET_VARIABLE = KEY_OP_LOOP_TARGET_VARIABLE
C.KEY_OP_LOOP_ITERABLE_REPR = KEY_OP_LOOP_ITERABLE_REPR
C.KEY_OP_LOOP_BODY_OPERATIONS = KEY_OP_LOOP_BODY_OPERATIONS
C.KEY_OP_ASSIGN_TO_OUTPUT = KEY_OP_ASSIGN_TO_OUTPUT

# --- Content from: ast_utils.py ---
def ast_node_to_repr_str(node):
    if isinstance(node, ast.Name): return f"Name(id='{node.id}')"
    elif isinstance(node, ast.Constant):
        val_type = type(node.value).__name__
        if isinstance(node.value, (int, float)): val_type = 'number' 
        elif isinstance(node.value, list) and not node.value: return "List(elts=[])" 
        return f"Constant(value_type='{val_type}')"
    elif isinstance(node, ast.Num): return f"Constant(value_type='number')" 
    elif isinstance(node, ast.List):
        if not node.elts: return "List(elts=[])"
        else: return f"List(elts=[{', '.join([ast_node_to_repr_str(e) for e in node.elts])}])"
    elif isinstance(node, ast.BinOp):
        op_map = {ast.Add: "Add", ast.Sub: "Sub", ast.Mult: "Mult", ast.Div: "Div", ast.FloorDiv: "FloorDiv", ast.Mod: "Mod", ast.Pow: "Pow"}
        op_str = op_map.get(type(node.op), type(node.op).__name__)
        left_repr = ast_node_to_repr_str(node.left)
        right_repr = ast_node_to_repr_str(node.right)
        return f"BinOp({left_repr}, {op_str}, {right_repr})"
    elif isinstance(node, ast.Call):
        func_repr = ast_node_to_repr_str(node.func)
        args_repr = [ast_node_to_repr_str(arg) for arg in node.args]
        keywords_repr_map = {kw.arg: ast_node_to_repr_str(kw.value) for kw in node.keywords}
        keywords_str = f", keywords={keywords_repr_map}" if keywords_repr_map else ""
        return f"Call(func={func_repr}, args=[{', '.join(args_repr)}]{keywords_str})"
    else: return f"UnsupportedASTNode({type(node).__name__})"

# --- Content from: ast_visitor.py (with the fix) ---
class HoloformGeneratorVisitor(ast.NodeVisitor):
    def __init__(self, source_code_lines_list):
        self.source_lines = source_code_lines_list
        self.holoform_data = {
            C.KEY_ID: "", C.KEY_PARENT_MODULE_ID: C.DEFAULT_PARENT_MODULE_ID,
            C.KEY_DESCRIPTION: C.DEFAULT_DESCRIPTION, C.KEY_TAGS: list(C.DEFAULT_TAGS), 
            C.KEY_INPUT_PARAMETERS: [], C.KEY_OPERATIONS: [], C.KEY_OUTPUT_VARIABLE_NAME: None
        }
        self.current_op_idx = 0; self.is_in_loop_body = False; self.loop_op_idx_stack = [] 

    def _get_current_op_idx_and_increment(self):
        if self.is_in_loop_body and self.loop_op_idx_stack:
            idx = self.loop_op_idx_stack[-1]; self.loop_op_idx_stack[-1] += 1; return idx
        else:
            idx = self.current_op_idx; self.current_op_idx += 1; return idx

    def _get_step_id(self, op_type_prefix):
        current_idx_val = self._get_current_op_idx_and_increment()
        return f"s_loop_{op_type_prefix}_{current_idx_val}" if self.is_in_loop_body else f"s_{op_type_prefix}_{current_idx_val}"

    def _get_comment_block_above_node(self, node_lineno):
        if node_lineno <= 1: return None
        comment_block_lines = []; current_line_idx = node_lineno - 2 
        while current_line_idx >= 0:
            line_content = self.source_lines[current_line_idx].strip()
            if line_content.startswith("#"): comment_block_lines.insert(0, self.source_lines[current_line_idx]) 
            elif not line_content: 
                if comment_block_lines: break 
            else: break
            current_line_idx -= 1
        return "\n".join(comment_block_lines) if comment_block_lines else None

    def visit_FunctionDef(self, node):
        self.holoform_data[C.KEY_ID] = f"{node.name}_auto_v1"
        docstring = ast.get_docstring(node, clean=False) 
        if docstring: self.holoform_data[C.KEY_DESCRIPTION] = docstring
        else:
            comments_above = self._get_comment_block_above_node(node.lineno)
            if comments_above: self.holoform_data[C.KEY_DESCRIPTION] = comments_above
        for arg in node.args.args: self.holoform_data[C.KEY_INPUT_PARAMETERS].append(arg.arg)
        self._process_body_nodes(node.body, self.holoform_data[C.KEY_OPERATIONS], extracted_docstring=docstring)

    def _process_body_nodes(self, body_nodes_list, target_operations_list, extracted_docstring=None):
        original_in_loop_body_state = self.is_in_loop_body
        for body_item_idx, body_item in enumerate(body_nodes_list):
            is_docstring_node = False
            if body_item_idx == 0 and extracted_docstring and isinstance(body_item, ast.Expr) and \
               isinstance(body_item.value, ast.Constant) and isinstance(body_item.value.value, str) and \
               body_item.value.value == extracted_docstring:
                is_docstring_node = True
            if is_docstring_node: continue
            elif isinstance(body_item, ast.Assign): self.visit_Assign(body_item, target_operations_list)
            elif isinstance(body_item, ast.Return): self.visit_Return(body_item, target_operations_list)
            elif isinstance(body_item, ast.For): self.visit_For(body_item, target_operations_list)
            elif isinstance(body_item, ast.Expr) and isinstance(body_item.value, ast.Call):
                self.visit_Call_Standalone(body_item.value, target_operations_list)
        self.is_in_loop_body = original_in_loop_body_state

    def visit_Assign(self, node, target_operations_list):
        base_op = {C.KEY_OP_STEP_ID: self._get_step_id("assign")}
        base_op[C.KEY_OP_ASSIGN_TO_VARIABLE] = node.targets[0].id if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) else "_complex_target_"
        op = {**base_op}
        if isinstance(node.value, ast.Call):
            call_node = node.value; op[C.KEY_OP_TYPE] = "function_call"
            op[C.KEY_OP_TARGET_FUNCTION_NAME] = call_node.func.id if isinstance(call_node.func, ast.Name) else "_complex_callable_"
            param_map = {}
            for kw in call_node.keywords:
                if isinstance(kw.value, ast.Name): param_map[kw.arg] = {"source_type": "variable", "name": kw.value.id}
                elif isinstance(kw.value, ast.Constant): param_map[kw.arg] = {"source_type": "constant", "value": kw.value.value}
                else: param_map[kw.arg] = {"source_type": "expression_ast", "repr": ast_node_to_repr_str(kw.value)}
            op[C.KEY_OP_PARAMETER_MAPPING] = param_map
        elif isinstance(node.value, ast.List) and not node.value.elts: 
            op[C.KEY_OP_EXPRESSION_TYPE] = "list_literal"; op[C.KEY_OP_EXPRESSION_AST_REPR] = ast_node_to_repr_str(node.value)
        else: 
            op[C.KEY_OP_EXPRESSION_TYPE] = "arithmetic"; op[C.KEY_OP_EXPRESSION_AST_REPR] = ast_node_to_repr_str(node.value)
        line_content = self.source_lines[node.lineno-1] if node.lineno > 0 and (node.lineno-1) < len(self.source_lines) else ""
        if line_content:
            cmt_idx = line_content.find("#")
            if cmt_idx != -1: op[C.KEY_OP_SEMANTIC_PURPOSE] = line_content[cmt_idx+1:].strip()
            else:
                verb = "Call & assign" if op.get(C.KEY_OP_TYPE) == "function_call" else "Init list" if op.get(C.KEY_OP_EXPRESSION_TYPE) == "list_literal" else "Assign val"
                op[C.KEY_OP_SEMANTIC_PURPOSE] = f"{verb} to '{op.get(C.KEY_OP_ASSIGN_TO_VARIABLE, '_')}'"
        else: op[C.KEY_OP_SEMANTIC_PURPOSE] = f"Assign to '{op.get(C.KEY_OP_ASSIGN_TO_VARIABLE, '_')}' (no line info)"
        target_operations_list.append(op)

    def visit_Call_Standalone(self, call_node, target_operations_list):
        op = {C.KEY_OP_STEP_ID: self._get_step_id("call_expr"), C.KEY_OP_TYPE: "function_call_standalone", C.KEY_OP_ASSIGN_TO_VARIABLE: None}
        op[C.KEY_OP_TARGET_FUNCTION_NAME] = call_node.func.id if isinstance(call_node.func, ast.Name) else "_complex_callable_"
        param_map = {}
        for i, arg_node in enumerate(call_node.args): param_map[f"arg{i}"] = {"source_type": "expression_ast", "repr": ast_node_to_repr_str(arg_node)}
        for kw in call_node.keywords:
            if isinstance(kw.value, ast.Name): param_map[kw.arg] = {"source_type": "variable", "name": kw.value.id}
            elif isinstance(kw.value, ast.Constant): param_map[kw.arg] = {"source_type": "constant", "value": kw.value.value}
            else: param_map[kw.arg] = {"source_type": "expression_ast", "repr": ast_node_to_repr_str(kw.value)}
        op[C.KEY_OP_PARAMETER_MAPPING] = param_map
        line_content = self.source_lines[call_node.lineno-1] if call_node.lineno > 0 and (call_node.lineno-1) < len(self.source_lines) else ""
        if line_content:
            cmt_idx = line_content.find("#")
            if cmt_idx != -1: op[C.KEY_OP_SEMANTIC_PURPOSE] = line_content[cmt_idx+1:].strip()
            else: op[C.KEY_OP_SEMANTIC_PURPOSE] = f"Execute call to '{op.get(C.KEY_OP_TARGET_FUNCTION_NAME, '_')}'"
        else: op[C.KEY_OP_SEMANTIC_PURPOSE] = f"Execute call (no line info)"
        target_operations_list.append(op)

    def visit_For(self, node, target_operations_list):
        loop_op = {
            C.KEY_OP_STEP_ID: self._get_step_id("loop"), C.KEY_OP_TYPE: "for_loop",
            C.KEY_OP_LOOP_TARGET_VARIABLE: node.target.id if isinstance(node.target, ast.Name) else "_complex_target_",
            C.KEY_OP_LOOP_ITERABLE_REPR: ast_node_to_repr_str(node.iter), C.KEY_OP_LOOP_BODY_OPERATIONS: []
        }
        line = self.source_lines[node.lineno-1] if node.lineno > 0 and (node.lineno-1) < len(self.source_lines) else ""
        if line:
            cmt_idx = line.find("#")
            if cmt_idx != -1: loop_op[C.KEY_OP_SEMANTIC_PURPOSE] = line[cmt_idx+1:].strip()
            else: loop_op[C.KEY_OP_SEMANTIC_PURPOSE] = f"Iterate over '{loop_op[C.KEY_OP_LOOP_ITERABLE_REPR]}' with '{loop_op[C.KEY_OP_LOOP_TARGET_VARIABLE]}'"
        else: loop_op[C.KEY_OP_SEMANTIC_PURPOSE] = f"Iterate (no line info)"
        target_operations_list.append(loop_op)
        self.is_in_loop_body = True; self.loop_op_idx_stack.append(0)
        self._process_body_nodes(node.body, loop_op[C.KEY_OP_LOOP_BODY_OPERATIONS], extracted_docstring=None)
        self.loop_op_idx_stack.pop()
        if not self.loop_op_idx_stack: self.is_in_loop_body = False 

    def visit_Return(self, node, target_ops_list): 
        if node.value and isinstance(node.value, ast.Name):
            self.holoform_data[C.KEY_OUTPUT_VARIABLE_NAME] = node.value.id
            for op in reversed(target_ops_list): 
                if op.get(C.KEY_OP_ASSIGN_TO_VARIABLE) == node.value.id:
                    op[C.KEY_OP_ASSIGN_TO_OUTPUT] = True; current_purpose = op.get(C.KEY_OP_SEMANTIC_PURPOSE, "")
                    verb = ""
                    if current_purpose.startswith("Assign val to"): verb = "Assign val"
                    elif current_purpose.startswith("Call & assign to"): verb = "Call & assign"
                    elif current_purpose.startswith("Init list to"): verb = "Init list"
                    if verb: op[C.KEY_OP_SEMANTIC_PURPOSE] = f"Set output '{node.value.id}' from: {verb} to '{node.value.id}'"
                    break 
        elif node.value:
            self.holoform_data[C.KEY_OUTPUT_VARIABLE_NAME] = "_direct_return_expression_"
            ret_op = {C.KEY_OP_STEP_ID: self._get_step_id("return_expr"), C.KEY_OP_ASSIGN_TO_OUTPUT: True,
                      C.KEY_OP_SEMANTIC_PURPOSE: "Return calculated expression directly", C.KEY_OP_EXPRESSION_TYPE: "arithmetic",
                      C.KEY_OP_EXPRESSION_AST_REPR: ast_node_to_repr_str(node.value)}
            target_ops_list.append(ret_op)

    def get_holoform(self):
        if self.holoform_data[C.KEY_DESCRIPTION] == C.DEFAULT_DESCRIPTION:
            op_summary = "its defined interface (no ops parsed)"
            if self.holoform_data.get(C.KEY_OPERATIONS):
                op_summary = self.holoform_data[C.KEY_OPERATIONS][0].get(C.KEY_OP_SEMANTIC_PURPOSE, 'its defined ops')
            self.holoform_data[C.KEY_DESCRIPTION] = f"Func '{self.holoform_data.get(C.KEY_ID,'_')}' for '{op_summary}'."
        current_desc = self.holoform_data[C.KEY_DESCRIPTION]
        if isinstance(current_desc, str):
            lines = current_desc.splitlines(); is_comment_block = False
            non_empty = [l for l in lines if l.strip()]
            if non_empty and all(l.lstrip().startswith("#") for l in non_empty): is_comment_block = True
            cleaned_lines = []
            for line in lines:
                stripped = line.lstrip()
                if is_comment_block: cleaned_lines.append(stripped[1:].lstrip() if stripped.startswith("#") else line)
                else: cleaned_lines.append(line)
            start_idx = 0; end_idx = len(cleaned_lines) - 1
            while start_idx < len(cleaned_lines) and not cleaned_lines[start_idx].strip(): start_idx += 1
            while end_idx >= start_idx and not cleaned_lines[end_idx].strip(): end_idx -=1
            self.holoform_data[C.KEY_DESCRIPTION] = "" if start_idx > end_idx else "\n".join(cleaned_lines[start_idx:end_idx+1])
        return self.holoform_data

# --- Content from: main_generator.py ---
def generate_holoform_from_code_string(code_str, function_name_target=None):
    try: parsed_ast = ast.parse(code_str)
    except SyntaxError as e: print(f"ERROR parsing code string: {e}"); return None
    source_lines = code_str.splitlines()
    for node in parsed_ast.body: 
        if isinstance(node, ast.FunctionDef) and (function_name_target is None or node.name == function_name_target):
            visitor = HoloformGeneratorVisitor(source_lines); visitor.visit(node); return visitor.get_holoform()
    return None

# --- Relevant Content from: test_code_strings.py ---
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
G_HELPER_GT_CORRECT_CODE_STR_WITH_DOCSTRING = """
# This is a comment above the function - should be ignored if docstring exists.
def G_helper_gt_correct_docstring(val1, val2):
    '''This is the primary docstring description.
    It has multiple lines.
    And some    leading spaces on this line.'''
    result = (val1 * 2) + val2 # The core calculation for docstring test
    return result
"""

# --- POC Integration Logic ---
def run_simulated_zero_in_poc_with_auto_holoforms():
    print("--- Starting Sub-Task 2.4: Simulated Zero-In POC with Auto-Generated Holoforms ---")
    print("\n[Phase 1: Defining Source Code Context]")
    code_context_g_helper = G_HELPER_GT_CORRECT_CODE_STR_WITH_DOCSTRING
    code_context_f_caller = F_CALLER_GT_CODE_STR
    print("Source for G_helper_gt_correct_docstring:\n" + "-"*20 + f"\n{code_context_g_helper}\n" + "-"*20)
    print("Source for F_caller_gt:\n" + "-"*20 + f"\n{code_context_f_caller}\n" + "-"*20)

    print("\n[Phase 2: Auto-Generating Holoforms using holoform_generators]")
    h_g_helper = generate_holoform_from_code_string(code_context_g_helper, "G_helper_gt_correct_docstring")
    h_f_caller = generate_holoform_from_code_string(code_context_f_caller, "F_caller_gt")

    if not h_f_caller or not h_g_helper:
        print("ERROR: Could not generate necessary Holoforms. Aborting."); return
    print(f"Successfully generated Holoform for: {h_f_caller['id']}")
    print(f"Successfully generated Holoform for: {h_g_helper['id']}")
    holoform_db = {h_f_caller['id']: h_f_caller, h_g_helper['id']: h_g_helper}
    print("Holoforms loaded into simulated DB.")

    print("\n[Phase 3: Simulating Zero-In Logic]")
    bug_report_query = {
        "entry_function_name": "F_caller_gt",
        "suspected_variable_in_entry": "helper_result_f", 
        "implication": "This variable comes from an external call, trace into it."
    }
    print(f"Processing simulated query: {bug_report_query}")
    explanation_log = []
    current_focus_holoform_id = f"{bug_report_query['entry_function_name']}_auto_v1"
    if current_focus_holoform_id not in holoform_db:
        print(f"ERROR: Entry Holoform '{current_focus_holoform_id}' not found. Aborting."); return
    explanation_log.append(f"1. Starting analysis with entry Holoform: '{current_focus_holoform_id}'.")
    current_holoform_data = holoform_db[current_focus_holoform_id]
    calling_operation = None
    for op in current_holoform_data.get("operations", []):
        if op.get("assign_to_variable") == bug_report_query["suspected_variable_in_entry"] and op.get("type") == "function_call":
            calling_operation = op
            explanation_log.append(f"2. Found operation '{op['step_id']}' in '{current_focus_holoform_id}' assigning to '{bug_report_query['suspected_variable_in_entry']}'.")
            explanation_log.append(f"   - Semantic Purpose: '{op['semantic_purpose']}'"); explanation_log.append(f"   - Calls function: '{op['target_function_name']}'."); break
    if not calling_operation:
        explanation_log.append(f"ERROR: No call op for '{bug_report_query['suspected_variable_in_entry']}' in '{current_focus_holoform_id}'."); print_explanation(explanation_log); return
    called_fn_short = calling_operation["target_function_name"]; called_fn_holo_id = f"{called_fn_short}_auto_v1"
    explanation_log.append(f"3. Traversing to called function's Holoform: '{called_fn_holo_id}'.")
    if called_fn_holo_id not in holoform_db:
        explanation_log.append(f"ERROR: Holoform for '{called_fn_holo_id}' not found."); print_explanation(explanation_log); return
    current_focus_holoform_id = called_fn_holo_id; current_holoform_data = holoform_db[current_focus_holoform_id]
    explanation_log.append(f"4. Focusing on Holoform: '{current_focus_holoform_id}'.")
    pinpointed_ops = []
    output_var = current_holoform_data.get("output_variable_name")
    explanation_log.append(f"   - Function '{called_fn_short}' expected to output: '{output_var}'.")
    for op in current_holoform_data.get("operations", []):
        if op.get("assign_to_output") is True or op.get("assign_to_variable") == output_var:
            pinpointed_ops.append(op)
            explanation_log.append(f"5. Pinpointed relevant op in '{current_focus_holoform_id}': Step ID: '{op['step_id']}', Purpose: '{op['semantic_purpose']}'")
    if not pinpointed_ops:
        explanation_log.append(f"Warning: No specific output op in '{current_focus_holoform_id}'.")
    print("\n[Phase 4: Zero-In Explanation]"); print_explanation(explanation_log)
    print("\n--- Sub-Task 2.4 Demonstration Complete ---")

def print_explanation(log_entries):
    print("-" * 40); [print(entry) for entry in log_entries]; print("-" * 40)

if __name__ == "__main__":
    run_simulated_zero_in_poc_with_auto_holoforms()
