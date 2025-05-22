# AIResearchProject/src/holoform_generators/main_generator.py
import ast
import json
from .ast_visitor import HoloformGeneratorVisitor # Import local visitor

def generate_holoform_from_code_string(code_str, function_name_target=None):
    """ 
    Main function to parse a Python code string and generate a Holoform 
    for a specific function or the first one found.
    """
    try:
        parsed_ast = ast.parse(code_str)
    except SyntaxError as e:
        print(f"ERROR parsing code string: {e}")
        return None
        
    source_lines = code_str.splitlines()
    
    for node in parsed_ast.body: # Iterate through top-level nodes in the module
        if isinstance(node, ast.FunctionDef):
            if function_name_target is None or node.name == function_name_target:
                # print(f"DEBUG: Processing function: {node.name} for Holoform generation...")
                # Pass the split source lines to the visitor for comment access
                visitor = HoloformGeneratorVisitor(source_lines) 
                visitor.visit(node) # Start visiting from the FunctionDef node
                return visitor.get_holoform()
    # print(f"DEBUG: Function '{function_name_target}' not found or no functions in code string.")
    return None
