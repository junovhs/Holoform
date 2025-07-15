import re

def execute_query(query, call_graph):
    """
    Executes an HQL query on a call graph.
    """
    match = re.match(r"MATCH \((\w+)\)-\[:CALLS\]->\((\w+)\) WHERE (\w+)\.id == \"(.*)\" RETURN (\w+)\.id", query)

    if match:
        caller_var = match.group(1)
        callee_var = match.group(2)
        where_var = match.group(3)
        callee_id = match.group(4)
        return_var = match.group(5)

        if where_var == callee_var and return_var == caller_var:
            results = []
            for caller, callees in call_graph.items():
                if callee_id in callees:
                    results.append(caller)
            return results

    return None
