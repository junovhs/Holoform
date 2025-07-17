import ast
from typing import Optional, List, Dict, Any, Union

class ImperativeBlockAnalyzer(ast.NodeVisitor):
    """A dedicated visitor to analyze a block of statements and find a 'Selection' pattern.
    This is the core of our pattern recognition engine for imperative code."""
    
    def __init__(self):
        self.pattern_found = False
        self.target_list = None
        self.source_iterable = None
        self.guard = "True"  # Default guard is always true if no if-statement
        self.transformation = None
        self.loop_variable = None
    
    def visit_Assign(self, node: ast.Assign):
        # Detect initialization: `output = []`
        if isinstance(node.value, ast.List) and not node.value.elts:
            if isinstance(node.targets[0], ast.Name):
                self.target_list = node.targets[0].id
        self.generic_visit(node)
    
    def visit_For(self, node: ast.For):
        # Find the loop components
        if isinstance(node.target, ast.Name):
            self.loop_variable = node.target.id
            self.source_iterable = DifferentialAnalyzer._format_expression(node.iter)
            
            # Visit the loop's body to find the guard and transformation
            for sub_node in node.body:
                self.visit(sub_node)
    
    def visit_If(self, node: ast.If):
        # Find the guard condition
        self.guard = DifferentialAnalyzer._format_expression(node.test)
        
        # Visit the if-statement's body to find the append call
        for sub_node in node.body:
            self.visit(sub_node)
    
    def visit_Expr(self, node: ast.Expr):
        # The append call is wrapped in an Expr node
        if isinstance(node.value, ast.Call):
            self.visit_Call(node.value)
    
    def visit_Call(self, node: ast.Call):
        # Detect the transformation: `target.append(transformation)`
        if isinstance(node.func, ast.Attribute) and node.func.attr == 'append':
            # Check if this append call is on the list we initialized
            if isinstance(node.func.value, ast.Name) and node.func.value.id == self.target_list:
                # The argument to append is our transformation
                self.transformation = DifferentialAnalyzer._format_expression(node.args[0])
                self.pattern_found = True


class StateModificationAnalyzer(ast.NodeVisitor):
    """Analyzes state modifications in code blocks."""
    
    def __init__(self):
        self.modifications = []
        self.current_guard = None
    
    def visit_If(self, node: ast.If):
        # Save the current guard
        old_guard = self.current_guard
        
        # Set the new guard for this if block
        self.current_guard = DifferentialAnalyzer._format_expression(node.test)
        
        # Visit the body with this guard context
        for sub_node in node.body:
            self.visit(sub_node)
        
        # Restore the previous guard
        self.current_guard = old_guard
        
        # Visit the else block if it exists
        if node.orelse:
            # If there's an else block, use the negation of the current guard
            if self.current_guard is None:
                else_guard = "else"
            else:
                else_guard = f"!({self.current_guard})"
            
            old_guard = self.current_guard
            self.current_guard = else_guard
            
            for sub_node in node.orelse:
                self.visit(sub_node)
            
            self.current_guard = old_guard
    
    def visit_Assign(self, node: ast.Assign):
        # Handle attribute assignments like obj.attr = value
        if isinstance(node.targets[0], ast.Attribute):
            target_obj = DifferentialAnalyzer._format_expression(node.targets[0].value)
            attr = node.targets[0].attr
            value = DifferentialAnalyzer._format_expression(node.value)
            
            self.modifications.append({
                "guard": self.current_guard,
                "target": f"{target_obj}.{attr}",
                "value": value
            })
        
        # Handle simple variable assignments
        elif isinstance(node.targets[0], ast.Name):
            target = node.targets[0].id
            value = DifferentialAnalyzer._format_expression(node.value)
            
            self.modifications.append({
                "guard": self.current_guard,
                "target": target,
                "value": value
            })
        
        # Handle subscript assignments like dict[key] = value
        elif isinstance(node.targets[0], ast.Subscript):
            target_obj = DifferentialAnalyzer._format_expression(node.targets[0].value)
            key = DifferentialAnalyzer._format_expression(node.targets[0].slice)
            value = DifferentialAnalyzer._format_expression(node.value)
            
            self.modifications.append({
                "guard": self.current_guard,
                "target": f"{target_obj}[{key}]",
                "value": value
            })


class ResourceManagementAnalyzer(ast.NodeVisitor):
    """Analyzes resource management patterns like 'with' statements and try-finally blocks."""
    
    def __init__(self):
        self.resources = []
    
    def visit_With(self, node: ast.With):
        # Process each with item (there can be multiple in a single with statement)
        for item in node.items:
            # Extract the resource acquisition expression
            resource_expr = DifferentialAnalyzer._format_expression(item.context_expr)
            
            # Extract the optional variable that will hold the resource
            if item.optional_vars and isinstance(item.optional_vars, ast.Name):
                var_name = item.optional_vars.id
            else:
                var_name = "_anonymous_resource"
            
            self.resources.append({
                "type": "with",
                "resource_expr": resource_expr,
                "var_name": var_name
            })
        
        # Visit the body of the with statement
        for sub_node in node.body:
            self.visit(sub_node)
    
    def visit_Try(self, node: ast.Try):
        # We're looking for try-finally patterns for resource management
        if node.finalbody:
            # Visit the try block
            for sub_node in node.body:
                self.visit(sub_node)
            
            # Check the finally block for resource cleanup
            for sub_node in node.finalbody:
                if isinstance(sub_node, ast.Expr) and isinstance(sub_node.value, ast.Call):
                    call = sub_node.value
                    if isinstance(call.func, ast.Attribute) and call.func.attr == 'close':
                        resource_obj = DifferentialAnalyzer._format_expression(call.func.value)
                        self.resources.append({
                            "type": "try-finally",
                            "resource_expr": "unknown",  # We don't know the acquisition expression from just the finally block
                            "var_name": resource_obj
                        })


class DifferentialAnalyzer:
    """V3: A semantic analyzer that reduces different syntaxes to a canonical HoloChain form.
    It uses pattern-matching visitors to understand behavior."""
    
    @staticmethod
    def _format_expression(node: ast.expr) -> str:
        # This is a simplified helper and can be expanded from ast_utils.py
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Constant):
            return repr(node.value)
        elif isinstance(node, ast.BinOp):
            left = DifferentialAnalyzer._format_expression(node.left)
            op_char = {ast.Add: '+', ast.Sub: '-', ast.Mult: '*', ast.Div: '/'}.get(type(node.op), '?')
            right = DifferentialAnalyzer._format_expression(node.right)
            return f"{left} {op_char} {right}"
        elif isinstance(node, ast.Compare):
            left = DifferentialAnalyzer._format_expression(node.left)
            op_char = {ast.Lt: '<', ast.Gt: '>', ast.Eq: '==', ast.NotEq: '!='}.get(type(node.ops[0]), '?')
            right = DifferentialAnalyzer._format_expression(node.comparators[0])
            return f"{left} {op_char} {right}"
        elif isinstance(node, ast.UnaryOp):
            if isinstance(node.op, ast.Not):
                operand = DifferentialAnalyzer._format_expression(node.operand)
                return f"!{operand}"
        elif isinstance(node, ast.Attribute):
            value = DifferentialAnalyzer._format_expression(node.value)
            return f"{value}.{node.attr}"
        elif isinstance(node, ast.Call):
            func = DifferentialAnalyzer._format_expression(node.func)
            args = [DifferentialAnalyzer._format_expression(arg) for arg in node.args]
            return f"{func}({', '.join(args)})"
        elif isinstance(node, ast.Subscript):
            value = DifferentialAnalyzer._format_expression(node.value)
            slice_val = DifferentialAnalyzer._format_expression(node.slice)
            return f"{value}[{slice_val}]"
        return "expr"
    
    def analyze_selection_pattern(self, code_block: str) -> str:
        """Analyzes a block of code to find a selection pattern."""
        try:
            tree = ast.parse(code_block.strip())
            
            # Attempt to find the complex "Imperative Selection" pattern first
            block_visitor = ImperativeBlockAnalyzer()
            block_visitor.visit(tree)
            
            if block_visitor.pattern_found:
                # Normalize the loop variable to 'x' for canonical output
                guard = block_visitor.guard.replace(f"{block_visitor.loop_variable}", "x")
                transformation = block_visitor.transformation.replace(f"{block_visitor.loop_variable}", "x")
                return f"S:{guard} <= {block_visitor.target_list}::{transformation}"
            
            # Fallback for single-statement declarative patterns
            if len(tree.body) == 1:
                node = tree.body[0]
                if isinstance(node, ast.Assign) and isinstance(node.value, ast.ListComp):
                    target_list = self._format_expression(node.targets[0])
                    generator = node.value.generators[0]
                    
                    # Handle the case with or without an if condition
                    if generator.ifs:
                        guard = self._format_expression(generator.ifs[0])
                    else:
                        guard = "True"
                    
                    transformation = self._format_expression(node.value.elt)
                    
                    # Normalize loop variable to 'x'
                    loop_var = generator.target.id
                    guard = guard.replace(loop_var, "x")
                    transformation = transformation.replace(loop_var, "x")
                    
                    return f"S:{guard} <= {target_list}::{transformation}"
        
        except Exception as e:
            return f"ANALYSIS_ERROR: {e}"
        
        return "UNANALYZED_PATTERN"
    
    def analyze_state_modification(self, code_block: str) -> str:
        """Analyzes a block of code to find state modification patterns."""
        try:
            tree = ast.parse(code_block.strip())
            
            # Use the state modification analyzer
            visitor = StateModificationAnalyzer()
            visitor.visit(tree)
            
            if visitor.modifications:
                # Convert the modifications to HoloChain format
                chains = []
                
                # Group modifications by their guard
                guard_groups = {}
                for mod in visitor.modifications:
                    guard = mod["guard"] if mod["guard"] is not None else "True"
                    if guard not in guard_groups:
                        guard_groups[guard] = []
                    guard_groups[guard].append(mod)
                
                # Create a chain for each guard group
                for guard, mods in guard_groups.items():
                    if guard == "True":
                        # No guard needed
                        chain = "G:"
                    else:
                        chain = f"G:{guard}->"
                    
                    # Add each modification to the chain
                    for i, mod in enumerate(mods):
                        if i > 0:
                            chain += "->"
                        chain += f"{mod['target']}={mod['value']}"
                    
                    chains.append(chain)
                
                return "\n".join(chains)
        
        except Exception as e:
            return f"ANALYSIS_ERROR: {e}"
        
        return "UNANALYZED_PATTERN"
    
    def analyze_resource_management(self, code_block: str) -> str:
        """Analyzes a block of code to find resource management patterns."""
        try:
            tree = ast.parse(code_block.strip())
            
            # Use the resource management analyzer
            visitor = ResourceManagementAnalyzer()
            visitor.visit(tree)
            
            if visitor.resources:
                # Convert the resources to HoloChain format
                chains = []
                
                for res in visitor.resources:
                    # Resource acquisition
                    chains.append(f"R:{res['resource_expr']} -> {res['var_name']}")
                    
                    # Resource release (guaranteed on block exit)
                    chains.append(f"G:block_exit({res['var_name']}) -> {res['var_name']}.close()")
                
                return "\n".join(chains)
        
        except Exception as e:
            return f"ANALYSIS_ERROR: {e}"
        
        return "UNANALYZED_PATTERN"
    
    def analyze(self, code_block: str) -> str:
        """Analyzes a block of code to find its core semantic pattern."""
        # Try each pattern analyzer in sequence
        result = self.analyze_selection_pattern(code_block)
        if result != "UNANALYZED_PATTERN":
            return result
        
        result = self.analyze_state_modification(code_block)
        if result != "UNANALYZED_PATTERN":
            return result
        
        result = self.analyze_resource_management(code_block)
        if result != "UNANALYZED_PATTERN":
            return result
        
        return "UNANALYZED_PATTERN"