def fibonacci(n):
    """Calculate the nth Fibonacci number."""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

class Calculator:
    def __init__(self):
        self.history = []
    
    def add(self, a, b):
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result
    
    def get_last_operation(self):
        return self.history[-1] if self.history else "No operations yet"

def process_numbers(numbers):
    """Process a list of numbers and return statistics."""
    if not numbers:
        return {"count": 0, "sum": 0, "avg": 0}
    
    total = sum(numbers)
    return {
        "count": len(numbers),
        "sum": total,
        "avg": total / len(numbers)
    }