#!/usr/bin/env python3
"""
Holoform Generator - Convert Python AST to structured JSON representations
Weekend Hacker Edition - Keep it under 250 lines
"""

import ast
import json
import sys
from typing import Dict, List, Any, Optional

class HoloformGenerator(ast.NodeVisitor):
    """Converts Python AST nodes into Holoform JSON structures"""
    
    def __init__(self):
        self.holoforms = []
        self.current_scope = []
    
    def visit_FunctionDef(self, node: ast.FunctionDef) -> Dict[str, Any]:
        """Convert function definition to Holoform"""
        holoform = {
            "type": "function",
            "name": node.name,
            "scope": ".".join(self.current_scope),
            "signature": {
                "args": [arg.arg for arg in node.args.args],
                "defaults": len(node.args.defaults),
                "returns": self._get_return_type(node)
            },
            "body_structure": self._analyze_body(node.body),
            "complexity": self._calculate_complexity(node),
            "dependencies": self._extract_dependencies(node)
        }
        
        docstring = ast.get_docstring(node)
        if docstring:
            holoform["docstring"] = docstring
        
        self.holoforms.append(holoform)
        return holoform
    
    def visit_ClassDef(self, node: ast.ClassDef) -> Dict[str, Any]:
        """Convert class definition to Holoform"""
        self.current_scope.append(node.name)
        
        holoform = {
            "type": "class",
            "name": node.name,
            "scope": ".".join(self.current_scope[:-1]),
            "bases": [self._node_to_string(base) for base in node.bases],
            "methods": [],
            "attributes": self._extract_attributes(node),
            "complexity": self._calculate_complexity(node)
        }
        
        docstring = ast.get_docstring(node)
        if docstring:
            holoform["docstring"] = docstring
        
        # Process methods
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                method_holoform = self.visit_FunctionDef(item)
                method_holoform["method_type"] = self._classify_method(item)
                holoform["methods"].append(method_holoform)
        
        self.current_scope.pop()
        self.holoforms.append(holoform)
        return holoform
    
    def _analyze_body(self, body: List[ast.stmt]) -> Dict[str, Any]:
        """Analyze function/method body structure"""
        structure = {
            "statements": len(body),
            "control_flow": [],
            "operations": [],
            "calls": []
        }
        
        for stmt in body:
            if isinstance(stmt, (ast.If, ast.For, ast.While)):
                structure["control_flow"].append(type(stmt).__name__.lower())
            elif isinstance(stmt, ast.Return):
                structure["operations"].append("return")
            elif isinstance(stmt, ast.Assign):
                structure["operations"].append("assign")
            elif isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
                call_name = self._node_to_string(stmt.value.func)
                structure["calls"].append(call_name)
        
        return structure
    
    def _calculate_complexity(self, node: ast.AST) -> int:
        """Simple cyclomatic complexity calculation"""
        complexity = 1  # Base complexity
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.Try)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        
        return complexity
    
    def _extract_dependencies(self, node: ast.AST) -> List[str]:
        """Extract function/variable dependencies"""
        deps = set()
        
        for child in ast.walk(node):
            if isinstance(child, ast.Name) and isinstance(child.ctx, ast.Load):
                deps.add(child.id)
            elif isinstance(child, ast.Call):
                func_name = self._node_to_string(child.func)
                if func_name:
                    deps.add(func_name)
        
        return sorted(list(deps))
    
    def _extract_attributes(self, node: ast.ClassDef) -> List[str]:
        """Extract class attributes from __init__ and assignments"""
        attributes = set()
        
        for item in node.body:
            if isinstance(item, ast.FunctionDef) and item.name == "__init__":
                for stmt in item.body:
                    if isinstance(stmt, ast.Assign):
                        for target in stmt.targets:
                            if isinstance(target, ast.Attribute) and \
                               isinstance(target.value, ast.Name) and \
                               target.value.id == "self":
                                attributes.add(target.attr)
        
        return sorted(list(attributes))
    
    def _classify_method(self, node: ast.FunctionDef) -> str:
        """Classify method type (constructor, property, etc.)"""
        if node.name == "__init__":
            return "constructor"
        elif node.name.startswith("__") and node.name.endswith("__"):
            return "dunder"
        elif node.name.startswith("_"):
            return "private"
        else:
            return "public"
    
    def _get_return_type(self, node: ast.FunctionDef) -> Optional[str]:
        """Extract return type annotation if present"""
        if node.returns:
            return self._node_to_string(node.returns)
        return None
    
    def _node_to_string(self, node: ast.AST) -> str:
        """Convert AST node to string representation"""
        try:
            return ast.unparse(node)
        except:
            return str(type(node).__name__)

def generate_holoforms(source_code: str) -> List[Dict[str, Any]]:
    """Main function to generate Holoforms from Python source code"""
    try:
        tree = ast.parse(source_code)
        generator = HoloformGenerator()
        generator.visit(tree)
        return generator.holoforms
    except SyntaxError as e:
        return [{"error": f"Syntax error: {e}"}]
    except Exception as e:
        return [{"error": f"Processing error: {e}"}]

def main():
    """CLI entry point"""
    if len(sys.argv) != 2:
        print("Usage: python holoform.py <python_file>")
        sys.exit(1)
    
    filename = sys.argv[1]
    
    try:
        with open(filename, 'r') as f:
            source_code = f.read()
        
        holoforms = generate_holoforms(source_code)
        print(json.dumps(holoforms, indent=2))
        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()