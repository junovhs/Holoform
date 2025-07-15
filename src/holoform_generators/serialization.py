import json

def serialize_holoform(holoform):
    """
    Serializes a Holoform to a human-readable textual format.
    """
    if not holoform:
        return "Invalid Holoform"

    if holoform.get("holoform_type") == "function":
        return _serialize_function_holoform(holoform)
    elif holoform.get("holoform_type") == "class":
        return _serialize_class_holoform(holoform)
    else:
        return "Unknown Holoform type"

def _serialize_function_holoform(holoform):
    """
    Serializes a function Holoform.
    """
    lines = []
    lines.append(f"Function: {holoform.get('id')}")
    lines.append(f"Description: {holoform.get('description')}")
    lines.append(f"Inputs: {', '.join(holoform.get('input_parameters', []))}")
    lines.append(f"Output: {holoform.get('output_variable_name')}")
    lines.append("Operations:")
    for op in holoform.get("operations", []):
        lines.append(f"  - {json.dumps(op)}")
    return "\n".join(lines)

def _serialize_class_holoform(holoform):
    """
    Serializes a class Holoform.
    """
    lines = []
    lines.append(f"Class: {holoform.get('id')}")
    lines.append(f"Description: {holoform.get('description')}")
    lines.append(f"Parent Classes: {', '.join(holoform.get('parent_classes', []))}")
    lines.append(f"Methods: {', '.join(holoform.get('methods', []))}")
    lines.append(f"Class Attributes: {', '.join(holoform.get('class_attributes', []))}")
    return "\n".join(lines)
