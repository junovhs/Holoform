class MyClass:
    def __init__(self):
        self.x = 0

    def increment(self):
        self.x += 1

def modify_state():
    """
    This function modifies the state of an instance of MyClass.
    """
    instance = MyClass()
    instance.increment()
    return instance.x
