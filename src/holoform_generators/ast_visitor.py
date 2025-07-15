# AIResearchProject/src/holoform_generators/ast_visitor.py
import ast
from . import constants as C
from .ast_utils import ast_node_to_repr_str

class HoloformGeneratorVisitor(ast.NodeVisitor):
    def __init__(self, source_code_lines_list):
        self.source_lines = source_code_lines_list
        self.holoform_data = {}
        self.current_op_idx = 0

    def _get_step_id(self, op_type_prefix):
        step_id = f"s_{op_type_prefix}_{self.current_op_idx}"
        self.current_op_idx += 1
        return step_id

    def visit(self, node):
        super().visit(node)
        return self.holoform_data

    def visit_FunctionDef(self, node):
        self.holoform_data = {
            "holoform_type": "function",
            C.KEY_ID: f"{node.name}_auto_v1",
            C.KEY_PARENT_MODULE_ID: C.DEFAULT_PARENT_MODULE_ID,
            C.KEY_DESCRIPTION: ast.get_docstring(node, clean=False) or C.DEFAULT_DESCRIPTION,
            C.KEY_TAGS: list(C.DEFAULT_TAGS),
            C.KEY_INPUT_PARAMETERS: [arg.arg for arg in node.args.args],
            C.KEY_OPERATIONS: [],
            C.KEY_OUTPUT_VARIABLE_NAME: None
        }
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self.holoform_data = {
            "holoform_type": "class",
            C.KEY_ID: f"{node.name}_auto_v1",
            C.KEY_PARENT_MODULE_ID: C.DEFAULT_PARENT_MODULE_ID,
            C.KEY_DESCRIPTION: ast.get_docstring(node, clean=False) or C.DEFAULT_DESCRIPTION,
            C.KEY_TAGS: list(C.DEFAULT_TAGS),
            "parent_classes": [ast_node_to_repr_str(base) for base in node.bases],
            "methods": [f.name for f in node.body if isinstance(f, ast.FunctionDef)],
            "class_attributes": [t.id for s in node.body if isinstance(s, ast.Assign) for t in s.targets if isinstance(t, ast.Name)]
        }
        # Don't visit children, we've handled them here
        return self.holoform_data

    def visit_Expr(self, node):
        if isinstance(node.value, ast.Call):
            self._handle_call(node, None)

    def visit_Assign(self, node):
        if len(node.targets) == 1:
            target = node.targets[0]
            if isinstance(target, ast.Name) and isinstance(node.value, ast.Call):
                self._handle_call(node, target.id)
            elif isinstance(target, ast.Name):
                self._handle_simple_assign(node, target.id)
            elif isinstance(target, ast.Attribute):
                self._handle_attribute_assign(node)
            elif isinstance(target, ast.Subscript):
                self._handle_subscript_assign(node)

        for op in self.holoform_data[C.KEY_OPERATIONS]:
            if op["step_id"] == self._get_step_id("assign") - 1:
                op["def_use"] = self._get_def_use(node)

    def visit_Return(self, node):
        if node.value:
            self.holoform_data[C.KEY_OUTPUT_VARIABLE_NAME] = ast_node_to_repr_str(node.value)

            operation = {
                "step_id": self._get_step_id("return"),
                "op_type": "return",
                "value": ast_node_to_repr_str(node.value),
                "def_use": self._get_def_use(node)
            }
            self.holoform_data[C.KEY_OPERATIONS].append(operation)

    def _handle_call(self, node, assign_to_variable):
        call_node = node.value
        func_name = self._get_name(call_node.func)
        op_type = "constructor_call" if func_name and func_name[0].isupper() else "function_call"

        operation = {
            "step_id": self._get_step_id(op_type),
            "op_type": op_type,
            "assign_to_variable": assign_to_variable,
            "target_function_name": func_name,
            "parameter_mapping": self._get_parameter_mapping(call_node)
        }
        if isinstance(call_node.func, ast.Attribute):
            operation["target_object"] = ast_node_to_repr_str(call_node.func.value)
        self.holoform_data[C.KEY_OPERATIONS].append(operation)

    def _handle_simple_assign(self, node, assign_to_variable):
        operation = {
            "step_id": self._get_step_id("assign"),
            "op_type": "assignment",
            "assign_to_variable": assign_to_variable,
            "value": ast_node_to_repr_str(node.value)
        }
        self.holoform_data[C.KEY_OPERATIONS].append(operation)

    def _handle_attribute_assign(self, node):
        target = node.targets[0]
        operation = {
            "step_id": self._get_step_id("attribute_assign"),
            "op_type": "state_modification",
            "subtype": "attribute_assignment",
            "target_object": ast_node_to_repr_str(target.value),
            "attribute": target.attr,
            "value": ast_node_to_repr_str(node.value)
        }
        self.holoform_data[C.KEY_OPERATIONS].append(operation)

    def _handle_subscript_assign(self, node):
        target = node.targets[0]
        operation = {
            "step_id": self._get_step_id("subscript_assign"),
            "op_type": "state_modification",
            "subtype": "dict_key_assignment",
            "target_dict": ast_node_to_repr_str(target.value),
            "key": ast_node_to_repr_str(target.slice),
            "value": ast_node_to_repr_str(node.value)
        }
        self.holoform_data[C.KEY_OPERATIONS].append(operation)

    def _get_name(self, func_node):
        if isinstance(func_node, ast.Name):
            return func_node.id
        if isinstance(func_node, ast.Attribute):
            return func_node.attr
        return None

    def _get_parameter_mapping(self, call_node):
        mapping = {}
        for i, arg in enumerate(call_node.args):
            mapping[f"arg{i}"] = ast_node_to_repr_str(arg)
        for kw in call_node.keywords:
            mapping[kw.arg] = ast_node_to_repr_str(kw.value)
        return mapping

    def _get_def_use(self, node):
        defs = []
        uses = []

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    defs.append(target.id)
            for value_node in ast.walk(node.value):
                if isinstance(value_node, ast.Name):
                    uses.append(value_node.id)
        elif isinstance(node, ast.Return):
            for value_node in ast.walk(node.value):
                if isinstance(value_node, ast.Name):
                    uses.append(value_node.id)

        return {"defs": defs, "uses": uses}

    def visit_If(self, node):
        test = ast_node_to_repr_str(node.test)
        body_visitor = HoloformGeneratorVisitor(self.source_lines)
        body = body_visitor.visit(node.body)

        orelse_visitor = HoloformGeneratorVisitor(self.source_lines)
        orelse = orelse_visitor.visit(node.orelse) if node.orelse else []

        operation = {
            "step_id": self._get_step_id("if"),
            "op_type": "control_flow",
            "subtype": "if",
            "test": test,
            "body": body["operations"],
            "orelse": orelse["operations"] if orelse else []
        }
        self.holoform_data[C.KEY_OPERATIONS].append(operation)

    def visit_While(self, node):
        test = ast_node_to_repr_str(node.test)
        body_visitor = HoloformGeneratorVisitor(self.source_lines)
        body = body_visitor.visit(node.body)

        operation = {
            "step_id": self._get_step_id("while"),
            "op_type": "control_flow",
            "subtype": "while",
            "test": test,
            "body": body["operations"]
        }
        self.holoform_data[C.KEY_OPERATIONS].append(operation)

    def visit_Try(self, node):
        body_visitor = HoloformGeneratorVisitor(self.source_lines)
        body = body_visitor.visit(node.body)

        handlers = []
        for handler in node.handlers:
            handler_visitor = HoloformGeneratorVisitor(self.source_lines)
            handler_body = handler_visitor.visit(handler.body)
            handlers.append({
                "type": ast_node_to_repr_str(handler.type) if handler.type else None,
                "name": handler.name,
                "body": handler_body["operations"]
            })

        finalbody_visitor = HoloformGeneratorVisitor(self.source_lines)
        finalbody = finalbody_visitor.visit(node.finalbody) if node.finalbody else []

        operation = {
            "step_id": self._get_step_id("try"),
            "op_type": "control_flow",
            "subtype": "try",
            "body": body["operations"],
            "handlers": handlers,
            "finalbody": finalbody["operations"] if finalbody else []
        }
        self.holoform_data[C.KEY_OPERATIONS].append(operation)
