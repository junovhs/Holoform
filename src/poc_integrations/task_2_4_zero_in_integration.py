import os
from src.holoform_generators.project_parser import parse_project

def simulated_zero_in(project_path, entry_point_func, bug_description):
    """
    Simulates the "zero-in" process of bug localization using a project-level call graph.
    """
    holoforms, call_graph = parse_project(project_path)

    print("--- Project Holoforms ---")
    for holoform in holoforms:
        print(holoform)

    print("\n--- Call Graph ---")
    print(call_graph)

    print(f"\n--- Simulating Zero-In ---")
    print(f"Entry Point: {entry_point_func}")
    print(f"Bug Description: {bug_description}")

    # This is a simplified simulation. A real implementation would involve
    # a more sophisticated analysis of the call graph and the bug description.

    entry_point_holoform_id = f"{entry_point_func}_auto_v1"
    if entry_point_holoform_id in call_graph:
        print(f"Analyzing call graph from entry point: {entry_point_holoform_id}")
        # In a real scenario, we would traverse the call graph and analyze the Holoforms
        # to identify the source of the bug. For this simulation, we will just print the
        # functions that are called directly from the entry point.
        callees = call_graph[entry_point_holoform_id]
        print(f"Potential bug sources (direct callees): {callees}")
    else:
        print(f"Entry point not found in call graph: {entry_point_holoform_id}")

if __name__ == '__main__':
    # Create a dummy project for testing
    os.makedirs("dummy_project", exist_ok=True)
    with open("dummy_project/main.py", "w") as f:
        f.write("""
def main():
    a = 1
    b = 2
    c = add(a, b)
    print(c)

def add(a, b):
    return a + b
""")

    simulated_zero_in("dummy_project", "main", "The program is not printing the correct sum.")