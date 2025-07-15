# Design Note: Holoform Query Language (HQL)

This document outlines the design for a conceptual query language for the Holoform graph, called the Holoform Query Language (HQL).

## 1. Research on Existing Graph Query Languages

I have researched the following graph query languages:

*   **Cypher:** A declarative query language for property graphs. It is used by the Neo4j graph database.
*   **GraphQL:** A query language for APIs that was developed by Facebook.
*   **SPARQL:** A query language for RDF data.

## 2. HQL Design

HQL is a declarative query language that is designed to be simple and easy to use. It is inspired by Cypher, but it is tailored to the specific needs of the Holoform graph.

The following is an example of an HQL query that finds all the callers of a function:

```
MATCH (caller)-[:CALLS]->(callee)
WHERE callee.id == "my_function_auto_v1"
RETURN caller.id
```

This query would return a list of the IDs of all the functions that call the `my_function` function.

## 3. HQL Grammar

The following is a simplified grammar for HQL:

```
query ::= match_clause [where_clause] return_clause

match_clause ::= "MATCH" "(" node_variable ")" "-" "[" relationship_variable "]" "->" "(" node_variable ")"

where_clause ::= "WHERE" expression

return_clause ::= "RETURN" expression ("," expression)*
```

## 4. Next Steps

The next step is to implement a prototype of the HQL query API. This will allow us to start experimenting with AI-assisted debugging and code understanding tasks.
