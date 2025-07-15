# Holoform Schema Specification

This document provides the formal specification for the Holoform data structure. It is intended to be a canonical reference for developers working on the Holoform generator, interpreters, and any other tools that interact with Holoforms.

## Versioning

This specification follows a semantic versioning scheme (e.g., `v1.0`, `v1.1`, `v2.0`). Any changes to the schema that are not backward-compatible will result in a major version increment. Additive, backward-compatible changes will result in a minor version increment.

**Current Version:** `v1.0`

## Holoform Structure

A Holoform is a JSON object that represents a single unit of code, such as a function, method, or class. The following sections define the fields in the Holoform object.

### Holoform Object Types

A Holoform can represent either a function or a class. The `holoform_type` field specifies which type of object the Holoform represents.

#### Function Holoform

A function Holoform represents a single function. It has the following schema:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Function Holoform v1.0",
  "description": "Schema for a single Holoform object, representing a function.",
  "type": "object",
  "properties": {
    "holoform_type": {
      "const": "function"
    },
    "id": {
      "description": "A unique identifier for the Holoform, typically derived from the function name.",
      "type": "string"
    },
    "parent_module_id": {
      "description": "The identifier of the module that contains this Holoform.",
      "type": "string"
    },
    "description": {
      "description": "A human-readable description of the Holoform's purpose, extracted from docstrings or comments.",
      "type": "string"
    },
    "tags": {
      "description": "A list of tags that categorize the Holoform.",
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "input_parameters": {
      "description": "A list of the names of the input parameters for the function.",
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "operations": {
      "description": "A list of the operations performed within the function.",
      "type": "array",
      "items": {
        "type": "object"
      }
    },
    "output_variable_name": {
      "description": "The name of the variable that is returned by the function.",
      "type": "string"
    }
  },
  "required": [
    "holoform_type",
    "id",
    "description",
    "input_parameters",
    "operations"
  ]
}
```

#### `runtime_phenomena`

The `runtime_phenomena` operation type represents advanced runtime phenomena that are difficult to represent with static analysis. It has the following subtypes:

*   **`dynamic_dispatch`**: Represents a dynamic method call.
*   **`reflection`**: Represents a reflection operation.
*   **`async_call`**: Represents an `async` function call.
*   **`io`**: Represents an I/O operation.

#### `control_flow`

The `control_flow` operation type represents control flow structures. It has the following subtypes:

*   **`if`**: Represents an `if/elif/else` structure.
*   **`while`**: Represents a `while` loop.
*   **`try`**: Represents a `try/except/finally` structure.

### Variable Definition-Use Chains

To represent variable definition-use chains, we will add a `def_use` field to each operation in the `operations` array. This field will be an object with two properties:

*   **`defs`**: A list of the variables that are defined in this operation.
*   **`uses`**: A list of the variables that are used in this operation.

#### Class Holoform

A class Holoform represents a single class. It has the following schema:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Class Holoform v1.0",
  "description": "Schema for a single Holoform object, representing a class.",
  "type": "object",
  "properties": {
    "holoform_type": {
      "const": "class"
    },
    "id": {
      "description": "A unique identifier for the Holoform, typically derived from the class name.",
      "type": "string"
    },
    "parent_module_id": {
      "description": "The identifier of the module that contains this Holoform.",
      "type": "string"
    },
    "description": {
      "description": "A human-readable description of the Holoform's purpose, extracted from docstrings or comments.",
      "type": "string"
    },
    "tags": {
      "description": "A list of tags that categorize the Holoform.",
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "parent_classes": {
      "description": "A list of the IDs of the parent classes.",
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "methods": {
      "description": "A list of the IDs of the method Holoforms.",
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "class_attributes": {
      "description": "A list of the class attributes.",
      "type": "array",
      "items": {
        "type": "string"
      }
    }
  },
  "required": [
    "holoform_type",
    "id",
    "description",
    "parent_classes",
    "methods",
    "class_attributes"
  ]
}
```

### Operation Subtypes

The `operations` array can contain a variety of different operation types. The following sections define the schemas for the different operation subtypes.

#### `state_modification`

The `state_modification` operation type represents a change to the state of an object. It has the following subtypes:

*   **`attribute_assignment`**: Represents the assignment of a value to an attribute of an object.
*   **`list_append`**: Represents the appending of an element to a list.
*   **`dict_key_assignment`**: Represents the assignment of a value to a key in a dictionary.

##### `attribute_assignment` Schema

```json
{
  "type": "object",
  "properties": {
    "op_type": {
      "const": "state_modification"
    },
    "subtype": {
      "const": "attribute_assignment"
    },
    "target_object": {
      "type": "string"
    },
    "attribute": {
      "type": "string"
    },
    "value": {
      "type": "string"
    }
  },
  "required": [
    "op_type",
    "subtype",
    "target_object",
    "attribute",
    "value"
  ]
}
```

##### `list_append` Schema

```json
{
  "type": "object",
  "properties": {
    "op_type": {
      "const": "state_modification"
    },
    "subtype": {
      "const": "list_append"
    },
    "target_list": {
      "type": "string"
    },
    "value": {
      "type": "string"
    }
  },
  "required": [
    "op_type",
    "subtype",
    "target_list",
    "value"
  ]
}
```

##### `dict_key_assignment` Schema

```json
{
  "type": "object",
  "properties": {
    "op_type": {
      "const": "state_modification"
    },
    "subtype": {
      "const": "dict_key_assignment"
    },
    "target_dict": {
      "type": "string"
    },
    "key": {
      "type": "string"
    },
    "value": {
      "type": "string"
    }
  },
  "required": [
    "op_type",
    "subtype",
    "target_dict",
    "key",
    "value"
  ]
}
```
