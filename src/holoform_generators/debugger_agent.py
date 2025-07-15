from .query_api import execute_query

def localize_bug(holoforms, call_graph, bug_report):
    """
    Localizes a bug in a project using the project-level Holoform graph.
    """
    entry_point = bug_report.get("entry_point")
    if not entry_point:
        return "No entry point specified in bug report."

    # Find all functions that are called directly or indirectly from the entry point.
    query = f"MATCH (caller)-[:CALLS*]->(callee) WHERE caller.id == \"{entry_point}_auto_v1\" RETURN callee.id"
    # This is a simplified query that does not handle transitive closures.
    # A real implementation would require a more sophisticated graph traversal algorithm.

    # For now, we will just find the direct callees.
    query = f"MATCH (caller)-[:CALLS]->(callee) WHERE caller.id == \"{entry_point}_auto_v1\" RETURN callee.id"

    potential_buggy_functions = execute_query(query, call_graph)

    if potential_buggy_functions:
        return f"Potential buggy functions: {potential_buggy_functions}"
    else:
        return "No potential buggy functions found."
