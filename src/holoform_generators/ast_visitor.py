# AIResearchProject/src/holoform_generators/ast_visitor.py
import ast
import re
from . import constants as C # Using local constants module
from .ast_utils import ast_node_to_repr_str # Using local ast_utils

class HoloformGeneratorVisitor(ast.NodeVisitor):
    def __init__(self, source_code_lines_list):
        self.source_lines = source_code_lines_list
        self.holoform_data = {
            C.KEY_ID: "", 
            C.KEY_PARENT_MODULE_ID: C.DEFAULT_PARENT_MODULE_ID,
            C.KEY_DESCRIPTION: C.DEFAULT_DESCRIPTION,
            C.KEY_TAGS: list(C.DEFAULT_TAGS), # Ensure it's a new list
            C.KEY_INPUT_PARAMETERS: [],
            C.KEY_OPERATIONS: [], 
            C.KEY_OUTPUT_VARIABLE_NAME: None
        }
        self.current_op_idx = 0
        self.is_in_loop_body = False
        self.loop_op_idx_stack = [] # To handle nested loops correctly

    def _get_current_op_idx_and_increment(self):
        if self.is_in_loop_body and self.loop_op_idx_stack:
            idx = self.loop_op_idx_stack[-1]
            self.loop_op_idx_stack[-1] += 1
            return idx
        else:
            idx = self.current_op_idx
            self.current_op_idx += 1
            return idx

    def _get_step_id(self, op_type_prefix):
        current_idx_val = self._get_current_op_idx_and_increment()
        if self.is_in_loop_body:
             return f"s_loop_{op_type_prefix}_{current_idx_val}"
        return f"s_{op_type_prefix}_{current_idx_val}"

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
        self.holoform_data[C.KEY_ID] = f"{node.name}_auto_v1"
        docstring = ast.get_docstring(node, clean=False) 
        if docstring: self.holoform_data[C.KEY_DESCRIPTION] = docstring
        else:
            comments_above = self._get_comment_block_above_node(node.lineno)
            if comments_above: self.holoform_data[C.KEY_DESCRIPTION] = comments_above
        
        for arg in node.args.args: self.holoform_data[C.KEY_INPUT_PARAMETERS].append(arg.arg)
        
        self._process_body_nodes(node.body, self.holoform_data[C.KEY_OPERATIONS])

    def _process_body_nodes(self, body_nodes_list, target_operations_list):
        original_in_loop_body_state = self.is_in_loop_body

        for body_item_idx, body_item in enumerate(body_nodes_list):
            is_docstring_node = False
            if not self.is_in_loop_body and body_item_idx == 0 and isinstance(body_item, ast.Expr) and \
               isinstance(body_item.value, ast.Constant) and \
               isinstance(body_item.value.value, str):
                # Check if it's the actual docstring by comparing with what ast.get_docstring would return
                # This node is the ast.Expr containing the docstring ast.Constant
                if hasattr(body_item.value, 'value') and ast.get_docstring(body_item.parent if hasattr(body_item, 'parent') else body_nodes_list[0].parent if hasattr(body_nodes_list[0],'parent') else None, clean=False) == body_item.value.value:
                     is_docstring_node = True
            
            if is_docstring_node: continue
            elif isinstance(body_item, ast.Assign): self.visit_Assign(body_item, target_operations_list)
            elif isinstance(body_item, ast.Return): self.visit_Return(body_item, target_operations_list)
            elif isinstance(body_item, ast.For):    self.visit_For(body_item, target_operations_list)
            elif isinstance(body_item, ast.Expr) and isinstance(body_item.value, ast.Call):
                self.visit_Call_Standalone(body_item.value, target_operations_list)
            # else: print(f"  WARNING: AST Gen unhandled node in body: {type(body_item)}")

        self.is_in_loop_body = original_in_loop_body_state

    def visit_Assign(self, node, target_operations_list):
        base_operation = { C.KEY_OP_STEP_ID: self._get_step_id("assign") }
        if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            base_operation[C.KEY_OP_ASSIGN_TO_VARIABLE] = node.targets[0].id
        else: base_operation[C.KEY_OP_ASSIGN_TO_VARIABLE] = "_complex_target_"

        operation = {**base_operation} # Start with base
        if isinstance(node.value, ast.Call):
            call_node = node.value
            operation[C.KEY_OP_TYPE] = "function_call"
            if isinstance(call_node.func, ast.Name): operation[C.KEY_OP_TARGET_FUNCTION_NAME] = call_node.func.id
            else: operation[C.KEY_OP_TARGET_FUNCTION_NAME] = "_complex_callable_"
            param_mapping = {}
            for kw in call_node.keywords:
                if isinstance(kw.value, ast.Name): param_mapping[kw.arg] = {"source_type": "variable", "name": kw.value.id}
                elif isinstance(kw.value, ast.Constant): param_mapping[kw.arg] = {"source_type": "constant", "value": kw.value.value}
                else: param_mapping[kw.arg] = {"source_type": "expression_ast", "repr": ast_node_to_repr_str(kw.value)}
            operation[C.KEY_OP_PARAMETER_MAPPING] = param_mapping
        elif isinstance(node.value, ast.List) and not node.value.elts: 
            operation[C.KEY_OP_EXPRESSION_TYPE] = "list_literal"
            operation[C.KEY_OP_EXPRESSION_AST_REPR] = ast_node_to_repr_str(node.value)
        else: 
            operation[C.KEY_OP_EXPRESSION_TYPE] = "arithmetic"
            operation[C.KEY_OP_EXPRESSION_AST_REPR] = ast_node_to_repr_str(node.value)
        
        if node.lineno > 0 and (node.lineno -1) < len(self.source_lines):
            assign_line_content = self.source_lines[node.lineno-1]; comment_idx = assign_line_content.find("#")
            if comment_idx != -1: operation[C.KEY_OP_SEMANTIC_PURPOSE] = assign_line_content[comment_idx+1:].strip()
            else:
                verb = "Call & assign" if operation.get(C.KEY_OP_TYPE) == "function_call" else "Init list" if operation.get(C.KEY_OP_EXPRESSION_TYPE) == "list_literal" else "Assign val"
                operation[C.KEY_OP_SEMANTIC_PURPOSE] = f"{verb} to '{operation.get(C.KEY_OP_ASSIGN_TO_VARIABLE, '_')}'"
        else: operation[C.KEY_OP_SEMANTIC_PURPOSE] = f"Assign to '{operation.get(C.KEY_OP_ASSIGN_TO_VARIABLE, '_')}' (no line info)"
        target_operations_list.append(operation)
    
    def visit_Call_Standalone(self, call_node, target_operations_list):
        operation = { C.KEY_OP_STEP_ID: self._get_step_id("call_expr"), C.KEY_OP_TYPE: "function_call_standalone", C.KEY_OP_ASSIGN_TO_VARIABLE: None }
        if isinstance(call_node.func, ast.Name): operation[C.KEY_OP_TARGET_FUNCTION_NAME] = call_node.func.id
        else: operation[C.KEY_OP_TARGET_FUNCTION_NAME] = "_complex_callable_"
        # Parameter mapping (same as in visit_Assign for calls)
        param_mapping = {}; # ... (can copy param mapping logic here)
        operation[C.KEY_OP_PARAMETER_MAPPING] = param_mapping
        # Semantic purpose (same as visit_Assign for calls)
        target_operations_list.append(operation)

    def visit_For(self, node, target_operations_list):
        loop_operation = {
            C.KEY_OP_STEP_ID: self._get_step_id("loop"), C.KEY_OP_TYPE: "for_loop",
            C.KEY_OP_LOOP_TARGET_VARIABLE: node.target.id if isinstance(node.target, ast.Name) else "_complex_target_",
            C.KEY_OP_LOOP_ITERABLE_REPR: ast_node_to_repr_str(node.iter),
            C.KEY_OP_LOOP_BODY_OPERATIONS: []
        }
        if node.lineno > 0 and (node.lineno - 1) < len(self.source_lines):
            for_line = self.source_lines[node.lineno - 1]; cmt_idx = for_line.find("#")
            if cmt_idx != -1: loop_operation[C.KEY_OP_SEMANTIC_PURPOSE] = for_line[cmt_idx + 1:].strip()
            else: loop_operation[C.KEY_OP_SEMANTIC_PURPOSE] = f"Iterate over '{loop_operation[C.KEY_OP_LOOP_ITERABLE_REPR]}' with '{loop_operation[C.KEY_OP_LOOP_TARGET_VARIABLE]}'"
        else: loop_operation[C.KEY_OP_SEMANTIC_PURPOSE] = f"Iterate (no line info)"
        target_operations_list.append(loop_operation)
        
        self.is_in_loop_body = True
        self.loop_op_idx_stack.append(0) # Push new counter for this loop's body
        self._process_body_nodes(node.body, loop_operation[C.KEY_OP_LOOP_BODY_OPERATIONS])
        self.loop_op_idx_stack.pop() # Pop counter for this loop's body
        if not self.loop_op_idx_stack: self.is_in_loop_body = False # Back to main body if no outer loops

    def visit_Return(self, node, source_operations_list):
        if node.value and isinstance(node.value, ast.Name):
            self.holoform_data[C.KEY_OUTPUT_VARIABLE_NAME] = node.value.id
            for op in reversed(source_operations_list):
                if op.get(C.KEY_OP_ASSIGN_TO_VARIABLE) == node.value.id:
                    op[C.KEY_OP_ASSIGN_TO_OUTPUT] = True
                    # Refine semantic purpose if it was generic assign
                    current_purpose = op.get(C.KEY_OP_SEMANTIC_PURPOSE, "")
                    if current_purpose.startswith("Assign val to") or current_purpose.startswith("Call & assign to") or current_purpose.startswith("Init list to"):
                        op[C.KEY_OP_SEMANTIC_PURPOSE] = f"Set output '{node.value.id}' from: {current_purpose}"
                    break 
        elif node.value:
             self.holoform_data[C.KEY_OUTPUT_VARIABLE_NAME] = "_direct_return_expression_"
             return_op = { C.KEY_OP_STEP_ID: self._get_step_id("return_expr"), C.KEY_OP_ASSIGN_TO_OUTPUT: True,
                           C.KEY_OP_SEMANTIC_PURPOSE: "Return calculated expression directly", C.KEY_OP_EXPRESSION_TYPE: "arithmetic",
                           C.KEY_OP_EXPRESSION_AST_REPR: ast_node_to_repr_str(node.value) }
             source_operations_list.append(return_op)
    
    def get_holoform(self):
        if self.holoform_data[C.KEY_DESCRIPTION] == C.DEFAULT_DESCRIPTION:
            op_summary = "its defined interface (no ops parsed)"
            if self.holoform_data[C.KEY_OPERATIONS]: op_summary = self.holoform_data[C.KEY_OPERATIONS][0].get(C.KEY_OP_SEMANTIC_PURPOSE, 'its defined ops')
            self.holoform_data[C.KEY_DESCRIPTION] = f"Func '{self.holoform_data.get(C.KEY_ID,'_')}' for '{op_summary}'."
        if isinstance(self.holoform_data[C.KEY_DESCRIPTION], str):
            cleaned_lines = []; is_comment_block = all(line.lstrip().startswith("#") for line in self.holoform_data[C.KEY_DESCRIPTION].strip().splitlines() if line.strip())
            for line in self.holoform_data[C.KEY_DESCRIPTION].splitlines():
                if is_comment_block: cleaned_lines.append(line.lstrip()[1:].lstrip() if line.lstrip().startswith("#") else line.strip())
                else: cleaned_lines.append(line) 
            if not is_comment_block and cleaned_lines:
                start_idx = 0; end_idx = len(cleaned_lines) -1
                while start_idx < len(cleaned_lines) and not cleaned_lines[start_idx].strip(): start_idx += 1
                while end_idx >= 0 and not cleaned_lines[end_idx].strip(): end_idx -=1
                self.holoform_data[C.KEY_DESCRIPTION] = "\n".join(cleaned_lines[start_idx:end_idx+1])
            else: self.holoform_data[C.KEY_DESCRIPTION] = "\n".join(cleaned_lines).strip()
        return self.holoform_data
