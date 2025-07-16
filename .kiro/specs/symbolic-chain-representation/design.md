# Design Document: Symbolic Chain Representation

## Overview

This design document outlines the approach for developing symbolic chain representation as an extreme token compression technique. Based on initial experiments achieving 97% token reduction, this system will create ultra-compressed representations of code behavior using symbolic notation while preserving semantic understanding for AI systems.

## Architecture

### Core Components

1. **Symbolic Notation Engine**: Converts code patterns into symbolic representations
2. **Chain Analyzer**: Identifies causal relationships and data flow patterns
3. **Compression Optimizer**: Minimizes token usage while preserving semantics
4. **Validation Framework**: Tests LLM comprehension of symbolic representations

### Design Principles

1. **Maximum Compression**: Achieve 90-97% token reduction from raw code
2. **Semantic Preservation**: Maintain essential information for code understanding
3. **Systematic Approach**: Use consistent rules for symbolic notation
4. **LLM Compatibility**: Ensure AI systems can interpret symbolic chains effectively

## Components and Interfaces

### HoloChain Symbol Vocabulary v0 Integration

Based on the comprehensive HoloChain specification, our symbolic chain representation will use the following structured approach:

#### Production Types
The system will generate 5 types of symbolic records:

```python
class HoloChainRecordTypes:
    FUNCTION = "F:"      # Function signature/meta: name(args)->rets
    GUARD = "G:"         # Guarded effect chain: cond -> effect -> effect  
    SELECT = "S:"        # Selection rule: expr <= target
    CONST = "C:"         # Constant/enum mapping: sym=value
    RETURN = "R:"        # Return/value derivation: expr -> out
```

#### Encoding Modes
```python
class EncodingMode:
    # Glyph Mode (GM) - Human readable
    GLYPH_ARROW = "→"
    GLYPH_ASSIGN = ":="
    GLYPH_SELECT = "⇐"
    
    # ASCII Compression Mode (ACM) - Token optimized
    ASCII_ARROW = "->"
    ASCII_ASSIGN = "="
    ASCII_SELECT = "<="
    
    # Logical operators (both modes)
    AND = "&&"
    OR = "||" 
    NOT = "!"
    CONDITIONAL = "?"
    ELSE = ":"
```

#### Core Grammar Elements
```python
# Comparison operators
COMPARISONS = ["==", "!=", ">", ">=", "<", "<="]

# Provenance format
PROVENANCE = "#<file>@L<line>"

# Context headers for namespacing
CONTEXT = "CTX:<module> <var_mappings>"
```

#### Pattern Templates
Common code patterns will have standardized symbolic representations:

```python
# Conditional state change: if condition then modify state
# Pattern: condition → state_change
# Example: email="" → status:=invalid → login_count:=0

# Function call chain: func1 calls func2 calls func3
# Pattern: func1 → func2 → func3
# Example: process_user → validate_user → update_stats

# Conditional logic: if A and B then C else D
# Pattern: (A & B) ? C : D
# Example: (critical & >8) ? add : skip
```

### Chain Analyzer

```python
class ChainAnalyzer:
    def __init__(self, holoform):
        self.holoform = holoform
        self.chains = []
    
    def identify_causal_chains(self):
        """Identify sequences of cause-effect relationships."""
        chains = []
        
        # Analyze state modifications
        state_chains = self._find_state_modification_chains()
        chains.extend(state_chains)
        
        # Analyze control flow
        control_chains = self._find_control_flow_chains()
        chains.extend(control_chains)
        
        # Analyze data flow
        data_chains = self._find_data_flow_chains()
        chains.extend(data_chains)
        
        return chains
    
    def _find_state_modification_chains(self):
        """Find chains where one state change leads to another."""
        # Example: empty email → invalid status → zero login count
        pass
    
    def _find_control_flow_chains(self):
        """Find chains of conditional logic."""
        # Example: critical type → priority check → add to results
        pass
    
    def _find_data_flow_chains(self):
        """Find chains of data transformation."""
        # Example: customer_id → customer data → discount rate → final price
        pass
```

### Symbolic Chain Generator

```python
class SymbolicChainGenerator:
    def __init__(self, notation_system):
        self.notation = notation_system
        self.compression_rules = CompressionRules()
    
    def generate_symbolic_chain(self, holoform, query_context=None):
        """Generate symbolic chain representation from Holoform."""
        
        # Analyze the Holoform for causal chains
        analyzer = ChainAnalyzer(holoform)
        chains = analyzer.identify_causal_chains()
        
        # Convert chains to symbolic notation
        symbolic_chains = []
        for chain in chains:
            symbolic_chain = self._convert_to_symbols(chain)
            symbolic_chains.append(symbolic_chain)
        
        # Apply compression rules
        compressed = self.compression_rules.optimize(symbolic_chains)
        
        # Format for specific query if provided
        if query_context:
            compressed = self._optimize_for_query(compressed, query_context)
        
        return compressed
    
    def _convert_to_symbols(self, chain):
        """Convert a causal chain to symbolic notation."""
        symbols = []
        
        for step in chain.steps:
            if step.type == "condition":
                symbols.append(self._format_condition(step))
            elif step.type == "state_change":
                symbols.append(self._format_state_change(step))
            elif step.type == "function_call":
                symbols.append(self._format_function_call(step))
        
        return self.notation.CAUSES.join(symbols)
    
    def _format_condition(self, condition):
        """Format conditional logic symbolically."""
        # Example: item["type"] == "critical" → (type=critical)
        # Example: priority > 8 → (>8)
        pass
    
    def _format_state_change(self, state_change):
        """Format state modifications symbolically."""
        # Example: user["status"] = "invalid" → status:=invalid
        pass
    
    def _format_function_call(self, function_call):
        """Format function calls symbolically."""
        # Example: get_discount_rate(customer) → discount_rate(cust)
        pass
```

### Compression Rules

```python
class CompressionRules:
    def __init__(self):
        self.abbreviations = {
            "customer": "cust",
            "priority": "pri",
            "status": "stat",
            "login_count": "login",
            "critical": "crit",
            "normal": "norm"
        }
        
        self.domain_shortcuts = {
            "email_empty": "email=\"\"",
            "gold_tier_5_years": "gold5y",
            "silver_tier_2_years": "silver2y"
        }
    
    def optimize(self, symbolic_chains):
        """Apply compression rules to minimize tokens."""
        optimized = []
        
        for chain in symbolic_chains:
            # Apply abbreviations
            compressed = self._apply_abbreviations(chain)
            
            # Apply domain-specific shortcuts
            compressed = self._apply_domain_shortcuts(compressed)
            
            # Remove redundant information
            compressed = self._remove_redundancy(compressed)
            
            optimized.append(compressed)
        
        return optimized
    
    def _apply_abbreviations(self, chain):
        """Replace common terms with shorter abbreviations."""
        for full_term, abbrev in self.abbreviations.items():
            chain = chain.replace(full_term, abbrev)
        return chain
    
    def _apply_domain_shortcuts(self, chain):
        """Replace common patterns with domain-specific shortcuts."""
        for pattern, shortcut in self.domain_shortcuts.items():
            chain = chain.replace(pattern, shortcut)
        return chain
    
    def _remove_redundancy(self, chain):
        """Remove redundant or implied information."""
        # Remove obvious type information
        # Combine related operations
        # Eliminate unnecessary intermediate steps
        return chain
```

## Data Models

### Symbolic Chain Structure

```python
class SymbolicChain:
    def __init__(self):
        self.chains = []           # List of causal chains
        self.context = {}          # Domain-specific context
        self.compression_ratio = 0 # Token reduction achieved
        self.query_optimized = False # Whether optimized for specific query
    
    def add_chain(self, chain_string, chain_type):
        """Add a symbolic chain with its type."""
        self.chains.append({
            'chain': chain_string,
            'type': chain_type,
            'tokens': len(chain_string.split())
        })
    
    def get_total_tokens(self):
        """Calculate total token count."""
        return sum(chain['tokens'] for chain in self.chains)
    
    def format_for_llm(self, query=None):
        """Format the symbolic chains for LLM consumption."""
        if query:
            # Include only chains relevant to the query
            relevant_chains = self._filter_relevant_chains(query)
            return "; ".join(chain['chain'] for chain in relevant_chains)
        else:
            return "; ".join(chain['chain'] for chain in self.chains)
```

## Testing Strategy

### Experimental Design

1. **Baseline Comparison**: Test symbolic chains against raw code and standard Holoforms
2. **Complexity Scaling**: Test on code examples of increasing complexity
3. **Domain Variation**: Test across different programming domains (web, data, algorithms)
4. **Query Specificity**: Test general vs. query-specific symbolic chains

### Metrics

1. **Token Efficiency**: Measure token reduction compared to raw code
2. **Semantic Fidelity**: Measure accuracy of LLM understanding
3. **Comprehension Speed**: Measure LLM response time
4. **Scalability**: Measure performance on larger code examples

### Test Cases

```python
test_cases = [
    {
        "name": "Simple State Chain",
        "code": "if not user.email: user.status = 'invalid'",
        "expected_symbolic": "email=\"\" → status:=invalid",
        "query": "What happens when email is empty?"
    },
    {
        "name": "Complex Conditional",
        "code": "if item.type == 'critical' and item.priority > 8: results.append(item)",
        "expected_symbolic": "(crit & >8) → add",
        "query": "When is item added to results?"
    },
    {
        "name": "Multi-Function Chain",
        "code": "customer = load_customer(id); rate = get_rate(customer); return apply_discount(total, rate)",
        "expected_symbolic": "id → cust → rate → discount(total)",
        "query": "How is discount calculated?"
    }
]
```

## Implementation Plan

1. **Phase 1**: Research and document symbolic notation principles
2. **Phase 2**: Implement basic symbolic chain generator
3. **Phase 3**: Test with LLMs and measure comprehension
4. **Phase 4**: Optimize based on results and refine notation
5. **Phase 5**: Integrate with existing Holoform system

This systematic approach will allow us to thoroughly explore the potential of symbolic chain representation while maintaining scientific rigor in our research methodology.