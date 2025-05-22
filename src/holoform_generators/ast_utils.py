# AIResearchProject/src/holoform_generators/ast_utils.py
import ast

def ast_node_to_repr_str(node):
    """Converts an AST expression node to a string representation of its structure."""
    if isinstance(node, ast.Name):
        return f"Name(id='{node.id}')"
    elif isinstance(node, ast.Constant):
        val_type = type(node.value).__name__
        if isinstance(node.value, (int, float)):
            val_type = 'number' # Generic type for numbers
        elif isinstance(node.value, list) and not node.value:
            return "List(elts=[])" # Specific representation for empty list constant
        return f"Constant(value_type='{val_type}')"
    elif isinstance(node, ast.Num): # For older Python (deprecated in 3.8)
        return f"Constant(value_type='number')" # Map to new Constant representation
    elif isinstance(node, ast.List):
        if not node.elts: # Empty list literal e.g. x = []
            return "List(elts=[])"
        else: # List with elements, more complex to represent, TBD if needed for current POCs
            return f"List(elts=[{', '.join([ast_node_to_repr_str(e) for e in node.elts])}])"
    elif isinstance(node, ast.BinOp):
        op_map = {
            ast.Add: "Add", ast.Sub: "Sub", ast.Mult: "Mult", ast.Div: "Div",
            ast.FloorDiv: "FloorDiv", ast.Mod: "Mod", ast.Pow: "Pow"
        }
        op_str = op_map.get(type(node.op), type(node.op).__name__)
        left_repr = ast_node_to_repr_str(node.left)
        right_repr = ast_node_to_repr_str(node.right)
        return f"BinOp({left_repr}, {op_str}, {right_repr})"
    elif isinstance(node, ast.Call):
        func_repr = ast_node_to_repr_str(node.func)
        args_repr = [ast_node_to_repr_str(arg) for arg in node.args]
        keywords_repr_map = {kw.arg: ast_node_to_repr_str(kw.value) for kw in node.keywords}
        # For cleaner output, only include keywords if present
        keywords_str = f", keywords={keywords_repr_map}" if keywords_repr_map else ""
        return f"Call(func={func_repr}, args=[{', '.join(args_repr)}]{keywords_str})"
    else:
        return f"UnsupportedASTNode({type(node).__name__})"
