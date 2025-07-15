import json

def calculate_semantic_compression_ratio(source_code, holoform):
    """
    Calculates the Semantic Compression Ratio (SCR) of a Holoform.
    """
    source_tokens = len(source_code.split())
    holoform_tokens = len(json.dumps(holoform).split())

    if source_tokens == 0:
        return 0

    return (source_tokens - holoform_tokens) / source_tokens

def calculate_semantic_fidelity_score(source_code, holoform):
    """
    Calculates the Semantic Fidelity Score (SFS) of a Holoform.
    This is a prototype and only considers variable preservation.
    """
    # For this prototype, we only consider variable preservation.
    # A more complete implementation would also consider operations,
    # control flow, and data dependencies.

    # Get all variables from the source code
    source_variables = set()
    for line in source_code.splitlines():
        for token in line.split():
            if token.isalpha() and token not in ["def", "class", "return"]:
                source_variables.add(token)

    # Get all variables from the Holoform
    holoform_variables = set()
    if "input_parameters" in holoform:
        for param in holoform["input_parameters"]:
            holoform_variables.add(param)
    if "operations" in holoform:
        for op in holoform["operations"]:
            if "assign_to_variable" in op:
                holoform_variables.add(op["assign_to_variable"])

    # Calculate the variable preservation score
    if not source_variables:
        return 1.0 if not holoform_variables else 0.0

    intersection = source_variables.intersection(holoform_variables)

    return len(intersection) / len(source_variables)
