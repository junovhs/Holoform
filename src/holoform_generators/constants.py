# AIResearchProject/src/holoform_generators/constants.py

# Default values for Holoform fields
DEFAULT_PARENT_MODULE_ID = "Unknown_Module_AST_v1"
DEFAULT_DESCRIPTION = "Auto-generated Holoform (default description)."
DEFAULT_TAGS = ["ast_generated"]

# AST Node representation constants (optional, could be part of a config)
# Example: How to represent unsupported nodes
UNSUPPORTED_NODE_PREFIX = "UnsupportedASTNode"

# Keys used in Holoform structure
KEY_ID = "id"
KEY_PARENT_MODULE_ID = "parent_module_id"
KEY_DESCRIPTION = "description"
KEY_TAGS = "tags"
KEY_INPUT_PARAMETERS = "input_parameters"
KEY_OPERATIONS = "operations"
KEY_OUTPUT_VARIABLE_NAME = "output_variable_name"
KEY_INTERNAL_VARIABLES = "internal_variables_config"

KEY_OP_STEP_ID = "step_id"
KEY_OP_TYPE = "type"
KEY_OP_EXPRESSION_TYPE = "expression_type"
KEY_OP_SEMANTIC_PURPOSE = "semantic_purpose"
KEY_OP_ASSIGN_TO_VARIABLE = "assign_to_variable"
KEY_OP_EXPRESSION_AST_REPR = "expression_ast_repr"
KEY_OP_ASSIGN_TO_OUTPUT = "assign_to_output"

KEY_OP_TARGET_FUNCTION_NAME = "target_function_name"
KEY_OP_PARAMETER_MAPPING = "parameter_mapping"

KEY_OP_LOOP_TARGET_VARIABLE = "target_variable"
KEY_OP_LOOP_ITERABLE_REPR = "iterable_source_repr"
KEY_OP_LOOP_BODY_OPERATIONS = "loop_body_operations"
