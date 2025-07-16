#!/usr/bin/env python3
"""
HoloChain Symbol Vocabulary v0 Parser
Converts Python code into HoloChain ACM (ASCII Compression Mode) format
"""

import ast
import re
from typing import List, Dict, Optional, Tuple

class HoloChainParser:
    """Parser that converts Python AST into HoloChain v0 symbolic representation."""
    
    def __init__(self, mode="ACM"):
        self.mode = mode  # ACM (ASCII Compression Mode) or GM (Glyph Mode)
        self.records = []
        self.context_vars = {}
        self.abbreviations = {
            "customer": "cust",
            "priority": "prio", 
            "status": "stat",
            "login_count": "login",
            "critical": "crit",
            "normal": "norm",
            "email": "email",
            "years": "yrs",
            "tier": "tier"
        }
        
        # Symbol mappings based on mode
        if mode == "ACM":
            self.ARROW = "->"
            self.ASSIGN = "="
            self.SELECT = "<="
        else:  # GM mode
            self.ARROW = "→"
            self.ASSIGN = ":="
            self.SELECT = "⇐"
    
    def parse_code(self, code: str, filename: str = "code.py") -> str:
        """Parse Python code and return HoloChain representation."""
        try:
            tree = ast.parse(code)
            self.records = []
            
            for node in tree.body:
                if isinstance(node, ast.FunctionDef):
                    self._parse_function(node, filename)
            
            return self._format_output()
            
        except SyntaxError as e:
            return f"# Syntax Error: {e}"
    
    def _parse_function(self, node: ast.FunctionDef, filename: str):
        """Parse a function definition into HoloChain records."""
        func_name = self._abbreviate(node.name)
        params = [self._abbreviate(arg.arg) for arg in node.args.args]
        
        # Add function signature
        param_str = ",".join(params)
        self.records.append(f"F:{func_name}({param_str})")
        
        # Parse function body for patterns
        self._parse_body(node.body, filename, node.lineno)
    
    def _parse_body(self, body: List[ast.stmt], filename: str, start_line: int):
        """Parse function body for HoloChain patterns."""
        for i, stmt in enumerate(body):
            line_no = getattr(stmt, 'lineno', start_line + i)
            
            if isinstance(stmt, ast.If):
                self._parse_if_statement(stmt, filename, line_no)
            elif isinstance(stmt, ast.Assign):
                self._parse_assignment(stmt, filename, line_no)
            elif isinstance(stmt, ast.Return):
                self._parse_return(stmt, filename, line_no)
            elif isinstance(stmt, ast.For):
                self._parse_for_loop(stmt, filename, line_no)
    
    def _parse_if_statement(self, node: ast.If, filename: str, line_no: int):
        """Parse if statement into Guard (G:) or Select (S:) records."""
        condition = self._format_condition(node.test)
        
        # Check if this is a selection pattern (append to collection)
        if self._is_selection_pattern(node.body):
            target = self._extract_selection_target(node.body)
            if target:
                prov = f"#{filename}@L{line_no}"
                self.records.append(f"S:{condition}{self.SELECT}{target}{prov}")
                return
        
        # Check if this is a guarded effect chain
        effects = self._extract_effects_chain(node.body)
        if effects:
            prov = f"#{filename}@L{line_no}"
            chain = f"G:{condition}{self.ARROW}{self.ARROW.join(effects)}{prov}"
            self.records.append(chain)
        
        # Handle elif/else chains
        if node.orelse:
            if len(node.orelse) == 1 and isinstance(node.orelse[0], ast.If):
                # elif case - use lowercase g: for secondary guards
                self._parse_elif_chain(node.orelse[0], filename, line_no)
            else:
                # else case
                else_effects = self._extract_effects_chain(node.orelse)
                if else_effects:
                    prov = f"#{filename}@L{line_no}"
                    chain = f"g:else{self.ARROW}{self.ARROW.join(else_effects)}{prov}"
                    self.records.append(chain)
    
    def _parse_elif_chain(self, node: ast.If, filename: str, line_no: int):
        """Parse elif chain into secondary guard records."""
        condition = self._format_condition(node.test)
        effects = self._extract_effects_chain(node.body)
        
        if effects:
            prov = f"#{filename}@L{line_no}"
            chain = f"g:{condition}{self.ARROW}{self.ARROW.join(effects)}{prov}"
            self.records.append(chain)
        
        # Continue with more elif/else
        if node.orelse:
            if len(node.orelse) == 1 and isinstance(node.orelse[0], ast.If):
                self._parse_elif_chain(node.orelse[0], filename, line_no)
            else:
                else_effects = self._extract_effects_chain(node.orelse)
                if else_effects:
                    prov = f"#{filename}@L{line_no}"
                    chain = f"g:else{self.ARROW}{self.ARROW.join(else_effects)}{prov}"
                    self.records.append(chain)
    
    def _parse_assignment(self, node: ast.Assign, filename: str, line_no: int):
        """Parse assignment statements."""
        if len(node.targets) == 1:
            target = node.targets[0]
            
            # Simple variable assignment
            if isinstance(target, ast.Name):
                var_name = self._abbreviate(target.id)
                value = self._format_expression(node.value)
                
                # Check if this is a constant definition
                if isinstance(node.value, (ast.Constant, ast.Num)):
                    prov = f"#{filename}@L{line_no}"
                    self.records.append(f"C:{var_name}{self.ASSIGN}{value}{prov}")
    
    def _parse_return(self, node: ast.Return, filename: str, line_no: int):
        """Parse return statements into Return (R:) records."""
        if node.value:
            expr = self._format_expression(node.value)
            prov = f"#{filename}@L{line_no}"
            
            # Try to identify the return variable name
            if isinstance(node.value, ast.Name):
                ret_var = self._abbreviate(node.value.id)
                self.records.append(f"R:{expr}{self.ARROW}{ret_var}{prov}")
            else:
                # Complex expression, use generic output name
                self.records.append(f"R:{expr}{self.ARROW}result{prov}")
    
    def _parse_for_loop(self, node: ast.For, filename: str, line_no: int):
        """Parse for loops - look for selection patterns."""
        # Check if loop body contains selection logic
        for stmt in node.body:
            if isinstance(stmt, ast.If):
                # This might be a selection pattern within a loop
                condition = self._format_condition(stmt.test)
                if self._is_selection_pattern(stmt.body):
                    target = self._extract_selection_target(stmt.body)
                    if target:
                        prov = f"#{filename}@L{line_no}"
                        self.records.append(f"S:{condition}{self.SELECT}{target}{prov}")
    
    def _format_condition(self, node: ast.expr) -> str:
        """Format a condition expression into HoloChain syntax."""
        if isinstance(node, ast.BoolOp):
            op = "&&" if isinstance(node.op, ast.And) else "||"
            values = [self._format_condition(v) for v in node.values]
            return f"({op.join(values)})"
        
        elif isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
            operand = self._format_condition(node.operand)
            return f"!{operand}"
        
        elif isinstance(node, ast.Compare):
            left = self._format_expression(node.left)
            if len(node.ops) == 1 and len(node.comparators) == 1:
                op = self._format_comparison_op(node.ops[0])
                right = self._format_expression(node.comparators[0])
                return f"{left}{op}{right}"
        
        return self._format_expression(node)
    
    def _format_comparison_op(self, op: ast.cmpop) -> str:
        """Format comparison operators."""
        op_map = {
            ast.Eq: "==",
            ast.NotEq: "!=", 
            ast.Lt: "<",
            ast.LtE: "<=",
            ast.Gt: ">",
            ast.GtE: ">="
        }
        return op_map.get(type(op), "==")
    
    def _format_expression(self, node: ast.expr) -> str:
        """Format an expression into HoloChain syntax."""
        if isinstance(node, ast.Name):
            return self._abbreviate(node.id)
        
        elif isinstance(node, ast.Constant):
            value = node.value
        elif hasattr(ast, 'Num') and isinstance(node, ast.Num):  # Python < 3.8 compatibility
            value = node.n
            if isinstance(value, str):
                return f'"{value}"' if value else '""'
            return str(value)
        
        elif isinstance(node, ast.Subscript):
            obj = self._format_expression(node.value)
            key = self._format_expression(node.slice)
            return f"{obj}[{key}]"
        
        elif isinstance(node, ast.Attribute):
            obj = self._format_expression(node.value)
            attr = self._abbreviate(node.attr)
            return f"{obj}.{attr}"
        
        elif isinstance(node, ast.BinOp):
            left = self._format_expression(node.left)
            right = self._format_expression(node.right)
            op_map = {
                ast.Add: "+", ast.Sub: "-", ast.Mult: "*", ast.Div: "/",
                ast.Mod: "%", ast.Pow: "**"
            }
            op = op_map.get(type(node.op), "+")
            return f"{left}{op}{right}"
        
        elif isinstance(node, ast.Call):
            func = self._format_expression(node.func)
            args = [self._format_expression(arg) for arg in node.args]
            return f"{func}({','.join(args)})"
        
        return "expr"
    
    def _is_selection_pattern(self, body: List[ast.stmt]) -> bool:
        """Check if body contains a selection pattern (append/add to collection)."""
        for stmt in body:
            if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
                if isinstance(stmt.value.func, ast.Attribute):
                    if stmt.value.func.attr in ["append", "add", "extend"]:
                        return True
        return False
    
    def _extract_selection_target(self, body: List[ast.stmt]) -> Optional[str]:
        """Extract the target collection for selection patterns."""
        for stmt in body:
            if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
                if isinstance(stmt.value.func, ast.Attribute):
                    if stmt.value.func.attr in ["append", "add", "extend"]:
                        target = self._format_expression(stmt.value.func.value)
                        return self._abbreviate(target)
        return None
    
    def _extract_effects_chain(self, body: List[ast.stmt]) -> List[str]:
        """Extract a chain of effects from a statement body."""
        effects = []
        
        for stmt in body:
            if isinstance(stmt, ast.Assign):
                if len(stmt.targets) == 1:
                    target = stmt.targets[0]
                    
                    if isinstance(target, ast.Name):
                        var = self._abbreviate(target.id)
                        value = self._format_expression(stmt.value)
                        effects.append(f"{var}{self.ASSIGN}{value}")
                    
                    elif isinstance(target, ast.Subscript):
                        obj = self._format_expression(target.value)
                        key = self._format_expression(target.slice)
                        value = self._format_expression(stmt.value)
                        effects.append(f"{obj}[{key}]{self.ASSIGN}{value}")
                    
                    elif isinstance(target, ast.Attribute):
                        obj = self._format_expression(target.value)
                        attr = self._abbreviate(target.attr)
                        value = self._format_expression(stmt.value)
                        effects.append(f"{obj}.{attr}{self.ASSIGN}{value}")
            
            elif isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
                # Function call as effect
                call_str = self._format_expression(stmt.value)
                effects.append(call_str)
        
        return effects
    
    def _abbreviate(self, name: str) -> str:
        """Apply abbreviation rules to variable/function names."""
        return self.abbreviations.get(name, name)
    
    def _format_output(self) -> str:
        """Format the collected records into final HoloChain output."""
        if not self.records:
            return "# No HoloChain patterns found"
        
        output = ["#HoloChain v0"]
        output.extend(self.records)
        return "\n".join(output)


def test_holochain_parser():
    """Test the HoloChain parser with our magic moment examples."""
    
    # Test case 1: Hidden state modification
    code1 = '''
def process_user_data(user_id):
    user = get_user(user_id)
    validate_user(user)
    update_user_stats(user)
    return user

def validate_user(user):
    if not user["email"]:
        user["status"] = "invalid"

def update_user_stats(user):
    if user["status"] == "invalid":
        user["login_count"] = 0
'''
    
    # Test case 2: Selection pattern
    code2 = '''
def analyze_data(items):
    results = []
    for item in items:
        if item["type"] == "critical" and item["priority"] > 8:
            results.append(item)
        elif item["type"] == "normal" and item["priority"] > 5:
            results.append(item)
    return results
'''
    
    # Test case 3: Tiered discount
    code3 = '''
def calculate_discount(customer_id, order_total):
    customer = load_customer(customer_id)
    if customer["tier"] == "gold" and customer["years"] >= 3:
        rate = 0.15
    elif customer["tier"] == "silver" and customer["years"] >= 2:
        rate = 0.10
    else:
        rate = 0.05
    return order_total * (1 - rate)
'''
    
    parser = HoloChainParser("ACM")
    
    print("=== Test Case 1: Hidden State Modification ===")
    result1 = parser.parse_code(code1, "user.py")
    print(result1)
    
    print("\n=== Test Case 2: Selection Pattern ===")
    result2 = parser.parse_code(code2, "data.py")
    print(result2)
    
    print("\n=== Test Case 3: Tiered Discount ===")
    result3 = parser.parse_code(code3, "discount.py")
    print(result3)


if __name__ == "__main__":
    test_holochain_parser()