# AIResearchProject/src/holoform_generators/main_generator.py
import ast
import json
from .ast_visitor import HoloformGeneratorVisitor # Import local visitor

def generate_holoform_from_code_string(code_str, target_name=None):
    """ 
    Main function to parse a Python code string and generate a Holoform 
    for a specific function or class, or the first one found.
    """
    try:
        parsed_ast = ast.parse(code_str)
    except SyntaxError as e:
        print(f"ERROR parsing code string: {e}")
        return None
        
    source_lines = code_str.splitlines()
    
    visitor = HoloformGeneratorVisitor(source_lines)
    for node in parsed_ast.body:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            if target_name is None or node.name == target_name:
                return visitor.visit(node)
    return None
