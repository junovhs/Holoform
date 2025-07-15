class MyClass:
    def greet(self):
        return "Hello!"

def call_method():
    """
    This function calls a method on an instance of MyClass.
    """
    instance = MyClass()
    return instance.greet()
