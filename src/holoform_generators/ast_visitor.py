# AIResearchProject/src/holoform_generators/ast_visitor.py
import ast
import re # Used for description cleaning, though ast.get_docstring(clean=True) also does some.
from . import constants as C 
from .ast_utils import ast_node_to_repr_str 

class HoloformGeneratorVisitor(ast.NodeVisitor):
    def __init__(self, source_code_lines_list):
        self.source_lines = source_code_lines_list
        self.holoform_data = {
            C.KEY_ID: "", 
            C.KEY_PARENT_MODULE_ID: C.DEFAULT_PARENT_MODULE_ID,
            C.KEY_DESCRIPTION: C.DEFAULT_DESCRIPTION,
            C.KEY_TAGS: list(C.DEFAULT_TAGS), 
            C.KEY_INPUT_PARAMETERS: [],
            C.KEY_OPERATIONS: [], 
            C.KEY_OUTPUT_VARIABLE_NAME: None
        }
        self.current_op_idx = 0
        self.is_in_loop_body = False
        self.loop_op_idx_stack = [] 

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
        # Extract docstring here first using the FunctionDef node
        docstring = ast.get_docstring(node, clean=False) 
        if docstring: 
            self.holoform_data[C.KEY_DESCRIPTION] = docstring
        else:
            # If no docstring, try to get comment block
            comments_above = self._get_comment_block_above_node(node.lineno)
            if comments_above: 
                self.holoform_data[C.KEY_DESCRIPTION] = comments_above
        
        for arg in node.args.args: self.holoform_data[C.KEY_INPUT_PARAMETERS].append(arg.arg)
        
        # Pass the already extracted docstring (or None) to _process_body_nodes
        # so it can reliably identify and skip the docstring Expr node.
        self._process_body_nodes(node.body, self.holoform_data[C.KEY_OPERATIONS], extracted_docstring=docstring)


    def _process_body_nodes(self, body_nodes_list, target_operations_list, extracted_docstring=None):
        original_in_loop_body_state = self.is_in_loop_body

        for body_item_idx, body_item in enumerate(body_nodes_list):
            is_docstring_node = False
            # Check if this body item is the docstring Expression node
            if body_item_idx == 0 and extracted_docstring and isinstance(body_item, ast.Expr):
                if isinstance(body_item.value, ast.Constant) and isinstance(body_item.value.value, str):
                    if body_item.value.value == extracted_docstring:
                        is_docstring_node = True
            
            if is_docstring_node: 
                continue # Skip the docstring node as it's handled as description
            elif isinstance(body_item, ast.Assign): 
                self.visit_Assign(body_item, target_operations_list)
            elif isinstance(body_item, ast.Return): 
                self.visit_Return(body_item, target_operations_list)
            elif isinstance(body_item, ast.For):    
                self.visit_For(body_item, target_operations_list)
            elif isinstance(body_item, ast.Expr) and isinstance(body_item.value, ast.Call):
                # This handles standalone calls like `my_function()` not assigned to anything
                self.visit_Call_Standalone(body_item.value, target_operations_list)
            # else: print(f"  WARNING: AST Gen unhandled node in body: {type(body_item)}")

        self.is_in_loop_body = original_in_loop_body_state

    def visit_Assign(self, node, target_operations_list):
        base_operation = { C.KEY_OP_STEP_ID: self._get_step_id("assign") }
        if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            base_operation[C.KEY_OP_ASSIGN_TO_VARIABLE] = node.targets[0].id
        else: base_operation[C.KEY_OP_ASSIGN_TO_VARIABLE] = "_complex_target_"

        operation = {**base_operation} 
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
        
        assign_line_content = self.source_lines[node.lineno-1] if node.lineno > 0 and (node.lineno -1) < len(self.source_lines) else ""
        if assign_line_content:
            comment_idx = assign_line_content.find("#")
            if comment_idx != -1: operation[C.KEY_OP_SEMANTIC_PURPOSE] = assign_line_content[comment_idx+1:].strip()
            else:
                verb = "Call & assign" if operation.get(C.KEY_OP_TYPE) == "function_call" else "Init list" if operation.get(C.KEY_OP_EXPRESSION_TYPE) == "list_literal" else "Assign val"
                operation[C.KEY_OP_SEMANTIC_PURPOSE] = f"{verb} to '{operation.get(C.KEY_OP_ASSIGN_TO_VARIABLE, '_')}'"
        else: operation[C.KEY_OP_SEMANTIC_PURPOSE] = f"Assign to '{operation.get(C.KEY_OP_ASSIGN_TO_VARIABLE, '_')}' (no line info)"
        target_operations_list.append(operation)
    
    def visit_Call_Standalone(self, call_node, target_operations_list):
        operation = { 
            C.KEY_OP_STEP_ID: self._get_step_id("call_expr"), 
            C.KEY_OP_TYPE: "function_call_standalone", 
            C.KEY_OP_ASSIGN_TO_VARIABLE: None 
        }
        if isinstance(call_node.func, ast.Name): 
            operation[C.KEY_OP_TARGET_FUNCTION_NAME] = call_node.func.id
        else: 
            operation[C.KEY_OP_TARGET_FUNCTION_NAME] = "_complex_callable_"
        
        param_mapping = {}
        # Positional arguments
        for i, arg_node in enumerate(call_node.args):
             param_mapping[f"arg{i}"] = {"source_type": "expression_ast", "repr": ast_node_to_repr_str(arg_node)} # Or more specific if Name/Constant
        # Keyword arguments
        for kw in call_node.keywords:
             if isinstance(kw.value, ast.Name): 
                 param_mapping[kw.arg] = {"source_type": "variable", "name": kw.value.id}
             elif isinstance(kw.value, ast.Constant): 
                 param_mapping[kw.arg] = {"source_type": "constant", "value": kw.value.value}
             else: 
                 param_mapping[kw.arg] = {"source_type": "expression_ast", "repr": ast_node_to_repr_str(kw.value)}
        operation[C.KEY_OP_PARAMETER_MAPPING] = param_mapping

        call_line_content = self.source_lines[call_node.lineno-1] if call_node.lineno > 0 and (call_node.lineno -1) < len(self.source_lines) else ""
        if call_line_content:
            comment_idx = call_line_content.find("#")
            if comment_idx != -1: 
                operation[C.KEY_OP_SEMANTIC_PURPOSE] = call_line_content[comment_idx+1:].strip()
            else: 
                operation[C.KEY_OP_SEMANTIC_PURPOSE] = f"Execute call to '{operation.get(C.KEY_OP_TARGET_FUNCTION_NAME, '_')}'"
        else: 
            operation[C.KEY_OP_SEMANTIC_PURPOSE] = f"Execute call (no line info)"
        target_operations_list.append(operation)

    def visit_For(self, node, target_operations_list):
        loop_operation = {
            C.KEY_OP_STEP_ID: self._get_step_id("loop"), C.KEY_OP_TYPE: "for_loop",
            C.KEY_OP_LOOP_TARGET_VARIABLE: node.target.id if isinstance(node.target, ast.Name) else "_complex_target_",
            C.KEY_OP_LOOP_ITERABLE_REPR: ast_node_to_repr_str(node.iter),
            C.KEY_OP_LOOP_BODY_OPERATIONS: []
        }
        for_line = self.source_lines[node.lineno - 1] if node.lineno > 0 and (node.lineno - 1) < len(self.source_lines) else ""
        if for_line:
            cmt_idx = for_line.find("#")
            if cmt_idx != -1: loop_operation[C.KEY_OP_SEMANTIC_PURPOSE] = for_line[cmt_idx + 1:].strip()
            else: loop_operation[C.KEY_OP_SEMANTIC_PURPOSE] = f"Iterate over '{loop_operation[C.KEY_OP_LOOP_ITERABLE_REPR]}' with '{loop_operation[C.KEY_OP_LOOP_TARGET_VARIABLE]}'"
        else: loop_operation[C.KEY_OP_SEMANTIC_PURPOSE] = f"Iterate (no line info)"
        target_operations_list.append(loop_operation)
        
        self.is_in_loop_body = True
        self.loop_op_idx_stack.append(0) 
        # Pass the current docstring status (should be None if inside loop body processing)
        self._process_body_nodes(node.body, loop_operation[C.KEY_OP_LOOP_BODY_OPERATIONS], extracted_docstring=None)
        self.loop_op_idx_stack.pop() 
        if not self.loop_op_idx_stack: self.is_in_loop_body = False 

    def visit_Return(self, node, target_operations_list): 
        if node.value and isinstance(node.value, ast.Name):
            self.holoform_data[C.KEY_OUTPUT_VARIABLE_NAME] = node.value.id
            for op in reversed(target_operations_list): 
                if op.get(C.KEY_OP_ASSIGN_TO_VARIABLE) == node.value.id:
                    op[C.KEY_OP_ASSIGN_TO_OUTPUT] = True
                    current_purpose = op.get(C.KEY_OP_SEMANTIC_PURPOSE, "")
                    # Refine semantic purpose if it was generic assign
                    verb_part = ""
                    if current_purpose.startswith("Assign val to"): verb_part = "Assign val"
                    elif current_purpose.startswith("Call & assign to"): verb_part = "Call & assign"
                    elif current_purpose.startswith("Init list to"): verb_part = "Init list"
                    
                    if verb_part:
                        op[C.KEY_OP_SEMANTIC_PURPOSE] = f"Set output '{node.value.id}' from: {verb_part} to '{node.value.id}'"
                    break 
        elif node.value:
             self.holoform_data[C.KEY_OUTPUT_VARIABLE_NAME] = "_direct_return_expression_"
             return_op = { 
                           C.KEY_OP_STEP_ID: self._get_step_id("return_expr"), 
                           C.KEY_OP_ASSIGN_TO_OUTPUT: True, # Conceptually, it's an output
                           C.KEY_OP_SEMANTIC_PURPOSE: "Return calculated expression directly", 
                           C.KEY_OP_EXPRESSION_TYPE: "arithmetic", # Or other based on ast_node_to_repr_str
                           C.KEY_OP_EXPRESSION_AST_REPR: ast_node_to_repr_str(node.value) 
                        }
             target_operations_list.append(return_op)
    
    def get_holoform(self):
        # Generate default description if needed (after all parsing)
        if self.holoform_data[C.KEY_DESCRIPTION] == C.DEFAULT_DESCRIPTION:
            op_summary = "its defined interface (no ops parsed)"
            if self.holoform_data.get(C.KEY_OPERATIONS): # Check if operations list is not empty
                op_summary = self.holoform_data[C.KEY_OPERATIONS][0].get(C.KEY_OP_SEMANTIC_PURPOSE, 'its defined ops')
            self.holoform_data[C.KEY_DESCRIPTION] = f"Func '{self.holoform_data.get(C.KEY_ID,'_')}' for '{op_summary}'."
        
        # Clean the final description (docstring or comment block)
        current_desc = self.holoform_data[C.KEY_DESCRIPTION]
        if isinstance(current_desc, str):
            lines = current_desc.splitlines()
            
            is_comment_block_heuristic = False
            non_empty_lines = [line for line in lines if line.strip()]
            if non_empty_lines and all(line.lstrip().startswith("#") for line in non_empty_lines):
                is_comment_block_heuristic = True

            cleaned_lines = []
            for line in lines:
                stripped_line = line.lstrip()
                if is_comment_block_heuristic:
                    if stripped_line.startswith("#"):
                        cleaned_lines.append(stripped_line[1:].lstrip()) 
                    else: 
                        cleaned_lines.append(line) # Should ideally not happen if heuristic is good
                else: # For docstrings, preserve internal indentation but strip surrounding blank lines
                    cleaned_lines.append(line) 
            
            # Remove leading/trailing blank lines from the potentially cleaned block
            start_idx = 0
            while start_idx < len(cleaned_lines) and not cleaned_lines[start_idx].strip():
                start_idx += 1
            
            end_idx = len(cleaned_lines) - 1
            while end_idx >= start_idx and not cleaned_lines[end_idx].strip():
                end_idx -= 1
            
            # Ensure we don't create an empty string if all lines were blank
            if start_idx > end_idx:
                self.holoform_data[C.KEY_DESCRIPTION] = ""
            else:
                self.holoform_data[C.KEY_DESCRIPTION] = "\n".join(cleaned_lines[start_idx:end_idx+1])
            
        return self.holoform_data