import unittest
import ast
from .ast_visitor import HoloformGeneratorVisitor
from . import constants as C

class TestNewVisitor(unittest.TestCase):
    def test_simple_function(self):
        code = """
def my_function(a, b):
    \"\"\"This is a simple function.\"\"\"
    c = a + b
    return c
"""
        visitor = HoloformGeneratorVisitor(code.splitlines())
        holoform = visitor.visit(ast.parse(code))

        self.assertEqual(holoform["holoform_type"], "function")
        self.assertEqual(holoform[C.KEY_ID], "my_function_auto_v1")
        self.assertEqual(holoform[C.KEY_DESCRIPTION], "This is a simple function.")
        self.assertEqual(holoform[C.KEY_INPUT_PARAMETERS], ["a", "b"])
        self.assertEqual(len(holoform[C.KEY_OPERATIONS]), 1)
        self.assertEqual(holoform[C.KEY_OPERATIONS][0]["op_type"], "assignment")
        self.assertEqual(holoform[C.KEY_OPERATIONS][0]["assign_to_variable"], "c")
        self.assertEqual(holoform[C.KEY_OPERATIONS][0]["value"], "BinOp(Name(id='a'), Add, Name(id='b'))")
        self.assertEqual(holoform[C.KEY_OUTPUT_VARIABLE_NAME], "Name(id='c')")

    def test_simple_class(self):
        code = """
class MyClass:
    \"\"\"This is a simple class.\"\"\"
    x = 1
    def my_method(self, a):
        return a + self.x
"""
        visitor = HoloformGeneratorVisitor(code.splitlines())
        holoform = visitor.visit(ast.parse(code))

        self.assertEqual(holoform["holoform_type"], "class")
        self.assertEqual(holoform[C.KEY_ID], "MyClass_auto_v1")
        self.assertEqual(holoform[C.KEY_DESCRIPTION], "This is a simple class.")
        self.assertEqual(holoform["parent_classes"], [])
        self.assertEqual(holoform["methods"], ["my_method"])
        self.assertEqual(holoform["class_attributes"], ["x"])

    def test_constructor_call(self):
        code = """
class MyClass:
    def __init__(self, name):
        self.name = name

def use_class():
    my_instance = MyClass("test")
"""
        visitor = HoloformGeneratorVisitor(code.splitlines())
        holoform = visitor.visit(ast.parse(code))

        self.assertEqual(len(holoform[C.KEY_OPERATIONS]), 1)
        self.assertEqual(holoform[C.KEY_OPERATIONS][0]["op_type"], "constructor_call")
        self.assertEqual(holoform[C.KEY_OPERATIONS][0]["target_function_name"], "MyClass")
        self.assertEqual(holoform[C.KEY_OPERATIONS][0]["assign_to_variable"], "my_instance")
        self.assertEqual(holoform[C.KEY_OPERATIONS][0]["parameter_mapping"], {"arg0": "Constant(value_type='str')"})

    def test_instance_method_call(self):
        code = """
class MyClass:
    def my_method(self, value):
        return value

def use_class():
    my_instance = MyClass()
    my_instance.my_method("test")
"""
        visitor = HoloformGeneratorVisitor(code.splitlines())
        holoform = visitor.visit(ast.parse(code))

        self.assertEqual(len(holoform[C.KEY_OPERATIONS]), 2)
        self.assertEqual(holoform[C.KEY_OPERATIONS][1]["op_type"], "function_call")
        self.assertEqual(holoform[C.KEY_OPERATIONS][1]["target_function_name"], "my_method")
        self.assertEqual(holoform[C.KEY_OPERATIONS][1]["target_object"], "Name(id='my_instance')")
        self.assertEqual(holoform[C.KEY_OPERATIONS][1]["parameter_mapping"], {"arg0": "Constant(value_type='str')"})

    def test_if_statement(self):
        code = """
def my_function(a):
    if a > 0:
        return "positive"
    else:
        return "not positive"
"""
        visitor = HoloformGeneratorVisitor(code.splitlines())
        holoform = visitor.visit(ast.parse(code))

        self.assertEqual(len(holoform[C.KEY_OPERATIONS]), 1)
        self.assertEqual(holoform[C.KEY_OPERATIONS][0]["op_type"], "control_flow")
        self.assertEqual(holoform[C.KEY_OPERATIONS][0]["subtype"], "if")
        self.assertEqual(holoform[C.KEY_OPERATIONS][0]["test"], "Compare(Name(id='a'), Gt, Constant(value_type='number'))")
        self.assertEqual(len(holoform[C.KEY_OPERATIONS][0]["body"]), 1)
        self.assertEqual(holoform[C.KEY_OPERATIONS][0]["body"][0]["op_type"], "return")
        self.assertEqual(len(holoform[C.KEY_OPERATIONS][0]["orelse"]), 1)
        self.assertEqual(holoform[C.KEY_OPERATIONS][0]["orelse"][0]["op_type"], "return")

    def test_while_loop(self):
        code = """
def my_function(a):
    while a > 0:
        a -= 1
"""
        visitor = HoloformGeneratorVisitor(code.splitlines())
        holoform = visitor.visit(ast.parse(code))

        self.assertEqual(len(holoform[C.KEY_OPERATIONS]), 1)
        self.assertEqual(holoform[C.KEY_OPERATIONS][0]["op_type"], "control_flow")
        self.assertEqual(holoform[C.KEY_OPERATIONS][0]["subtype"], "while")
        self.assertEqual(holoform[C.KEY_OPERATIONS][0]["test"], "Compare(Name(id='a'), Gt, Constant(value_type='number'))")
        self.assertEqual(len(holoform[C.KEY_OPERATIONS][0]["body"]), 1)
        self.assertEqual(holoform[C.KEY_OPERATIONS][0]["body"][0]["op_type"], "assignment")

    def test_try_except(self):
        code = """
def my_function():
    try:
        a = 1 / 0
    except ZeroDivisionError:
        a = 0
"""
        visitor = HoloformGeneratorVisitor(code.splitlines())
        holoform = visitor.visit(ast.parse(code))

        self.assertEqual(len(holoform[C.KEY_OPERATIONS]), 1)
        self.assertEqual(holoform[C.KEY_OPERATIONS][0]["op_type"], "control_flow")
        self.assertEqual(holoform[C.KEY_OPERATIONS][0]["subtype"], "try")
        self.assertEqual(len(holoform[C.KEY_OPERATIONS][0]["body"]), 1)
        self.assertEqual(holoform[C.KEY_OPERATIONS][0]["body"][0]["op_type"], "assignment")
        self.assertEqual(len(holoform[C.KEY_OPERATIONS][0]["handlers"]), 1)
        self.assertEqual(holoform[C.KEY_OPERATIONS][0]["handlers"][0]["type"], "Name(id='ZeroDivisionError')")
        self.assertEqual(len(holoform[C.KEY_OPERATIONS][0]["handlers"][0]["body"]), 1)
        self.assertEqual(holoform[C.KEY_OPERATIONS][0]["handlers"][0]["body"][0]["op_type"], "assignment")

    def test_data_flow(self):
        code = """
def my_function(a, b):
    c = a + b
    d = c * 2
    return d
"""
        visitor = HoloformGeneratorVisitor(code.splitlines())
        holoform = visitor.visit(ast.parse(code))

        self.assertEqual(len(holoform[C.KEY_OPERATIONS]), 3)
        self.assertEqual(holoform[C.KEY_OPERATIONS][0]["def_use"]["defs"], ["c"])
        self.assertEqual(holoform[C.KEY_OPERATIONS][0]["def_use"]["uses"], ["a", "b"])
        self.assertEqual(holoform[C.KEY_OPERATIONS][1]["def_use"]["defs"], ["d"])
        self.assertEqual(holoform[C.KEY_OPERATIONS][1]["def_use"]["uses"], ["c"])
        self.assertEqual(holoform[C.KEY_OPERATIONS][2]["def_use"]["defs"], [])
        self.assertEqual(holoform[C.KEY_OPERATIONS][2]["def_use"]["uses"], ["d"])

if __name__ == '__main__':
    unittest.main()
