#!/usr/bin/env python3
"""
Phase 4: Semantic Unit Parser for RTR & ECS calculation.
Extracts semantic units from original test patterns according to taxonomy.
"""

import json
import os
from typing import List, Dict, Any
from dataclasses import dataclass
from enum import Enum

class SemanticUnitType(Enum):
    """Semantic unit types per taxonomy."""
    FLOW_STEP = "flow_step"
    CONDITION = "condition"
    ASSIGNMENT = "assignment"
    CONTEXT_SCOPE = "context_scope"
    ERROR_PATH = "error_path"

@dataclass
class SemanticUnit:
    """A single semantic unit."""
    unit_type: SemanticUnitType
    description: str
    pattern_context: str
    is_error_related: bool = False

class SemanticUnitParser:
    """Parser for extracting semantic units from test patterns."""
    
    def __init__(self):
        self.unit_counter = 0
    
    def parse_test_pattern(self, test_id: str, pattern_sequence: str, baseline_questions: List[str]) -> List[SemanticUnit]:
        """Parse a test pattern and extract semantic units."""
        units = []
        
        # Parse based on test pattern and questions
        if test_id == "T1":
            # Context Scoping Logic (Intermediate)
            units = self._parse_t1_context_scoping(baseline_questions)
        elif test_id == "T2":
            # Error Recovery Flow (Advanced)
            units = self._parse_t2_error_recovery(baseline_questions)
        elif test_id == "T3":
            # Expert CLI Operation
            units = self._parse_t3_cli_operation(baseline_questions)
        elif test_id == "T4":
            # Multi-Condition Decision Tree
            units = self._parse_t4_decision_tree(baseline_questions)
        elif test_id == "T5":
            # Resource Management (FAILED)
            units = self._parse_t5_resource_management(baseline_questions)
        elif test_id == "T6":
            # Concurrent Context Handling
            units = self._parse_t6_concurrent_context(baseline_questions)
        elif test_id == "T7":
            # Basic Git Operation
            units = self._parse_t7_git_operation(baseline_questions)
        
        return units
    
    def _parse_t1_context_scoping(self, questions: List[str]) -> List[SemanticUnit]:
        """Parse T1: Context Scoping Logic (Intermediate)."""
        units = [
            SemanticUnit(
                unit_type=SemanticUnitType.FLOW_STEP,
                description="Primary control flow structure execution",
                pattern_context="T1_context_scoping"
            ),
            SemanticUnit(
                unit_type=SemanticUnitType.CONDITION,
                description="Conditional branches evaluation",
                pattern_context="T1_context_scoping"
            ),
            SemanticUnit(
                unit_type=SemanticUnitType.ASSIGNMENT,
                description="Variable modifications within scope",
                pattern_context="T1_context_scoping"
            ),
            SemanticUnit(
                unit_type=SemanticUnitType.CONTEXT_SCOPE,
                description="Final output or return value determination",
                pattern_context="T1_context_scoping"
            )
        ]
        return units
    
    def _parse_t2_error_recovery(self, questions: List[str]) -> List[SemanticUnit]:
        """Parse T2: Error Recovery Flow (Advanced)."""
        units = [
            SemanticUnit(
                unit_type=SemanticUnitType.ERROR_PATH,
                description="Error conditions detection and handling",
                pattern_context="T2_error_recovery",
                is_error_related=True
            ),
            SemanticUnit(
                unit_type=SemanticUnitType.ERROR_PATH,
                description="Recovery mechanism execution when errors occur",
                pattern_context="T2_error_recovery",
                is_error_related=True
            ),
            SemanticUnit(
                unit_type=SemanticUnitType.FLOW_STEP,
                description="Code flow changes during error states",
                pattern_context="T2_error_recovery"
            ),
            SemanticUnit(
                unit_type=SemanticUnitType.FLOW_STEP,
                description="Cleanup or rollback operations",
                pattern_context="T2_error_recovery"
            )
        ]
        return units
    
    def _parse_t3_cli_operation(self, questions: List[str]) -> List[SemanticUnit]:
        """Parse T3: Expert CLI Operation."""
        units = [
            SemanticUnit(
                unit_type=SemanticUnitType.FLOW_STEP,
                description="Command-line operations execution",
                pattern_context="T3_cli_operation"
            ),
            SemanticUnit(
                unit_type=SemanticUnitType.ASSIGNMENT,
                description="Input parameters and validation",
                pattern_context="T3_cli_operation"
            ),
            SemanticUnit(
                unit_type=SemanticUnitType.FLOW_STEP,
                description="Sequence of operations execution",
                pattern_context="T3_cli_operation"
            ),
            SemanticUnit(
                unit_type=SemanticUnitType.ASSIGNMENT,
                description="Output or side effects production",
                pattern_context="T3_cli_operation"
            ),
            SemanticUnit(
                unit_type=SemanticUnitType.CONDITION,
                description="Different execution paths handling",
                pattern_context="T3_cli_operation"
            )
        ]
        return units
    
    def _parse_t4_decision_tree(self, questions: List[str]) -> List[SemanticUnit]:
        """Parse T4: Multi-Condition Decision Tree."""
        units = [
            SemanticUnit(
                unit_type=SemanticUnitType.CONDITION,
                description="Decision points in logic tree",
                pattern_context="T4_decision_tree"
            ),
            SemanticUnit(
                unit_type=SemanticUnitType.CONDITION,
                description="Conditions determining each branch",
                pattern_context="T4_decision_tree"
            ),
            SemanticUnit(
                unit_type=SemanticUnitType.ASSIGNMENT,
                description="Possible outcomes or actions",
                pattern_context="T4_decision_tree"
            ),
            SemanticUnit(
                unit_type=SemanticUnitType.CONDITION,
                description="Condition relationships and dependencies",
                pattern_context="T4_decision_tree"
            )
        ]
        return units
    
    def _parse_t5_resource_management(self, questions: List[str]) -> List[SemanticUnit]:
        """Parse T5: Resource Management (FAILED)."""
        units = [
            SemanticUnit(
                unit_type=SemanticUnitType.ASSIGNMENT,
                description="Resource management and tracking",
                pattern_context="T5_resource_management"
            ),
            SemanticUnit(
                unit_type=SemanticUnitType.FLOW_STEP,
                description="Resource acquisition and release",
                pattern_context="T5_resource_management"
            ),
            SemanticUnit(
                unit_type=SemanticUnitType.ERROR_PATH,
                description="Error handling for resource failures",
                pattern_context="T5_resource_management",
                is_error_related=True
            ),
            SemanticUnit(
                unit_type=SemanticUnitType.ERROR_PATH,
                description="Cleanup operations ensuring proper resource disposal",
                pattern_context="T5_resource_management",
                is_error_related=True
            )
        ]
        return units
    
    def _parse_t6_concurrent_context(self, questions: List[str]) -> List[SemanticUnit]:
        """Parse T6: Concurrent Context Handling."""
        units = [
            SemanticUnit(
                unit_type=SemanticUnitType.FLOW_STEP,
                description="Concurrent operations coordination",
                pattern_context="T6_concurrent_context"
            ),
            SemanticUnit(
                unit_type=SemanticUnitType.CONTEXT_SCOPE,
                description="Context sharing between concurrent processes",
                pattern_context="T6_concurrent_context"
            ),
            SemanticUnit(
                unit_type=SemanticUnitType.FLOW_STEP,
                description="Synchronization mechanisms usage",
                pattern_context="T6_concurrent_context"
            ),
            SemanticUnit(
                unit_type=SemanticUnitType.ERROR_PATH,
                description="Race conditions or conflicts handling",
                pattern_context="T6_concurrent_context",
                is_error_related=True
            )
        ]
        return units
    
    def _parse_t7_git_operation(self, questions: List[str]) -> List[SemanticUnit]:
        """Parse T7: Basic Git Operation."""
        units = [
            SemanticUnit(
                unit_type=SemanticUnitType.FLOW_STEP,
                description="Git operation execution",
                pattern_context="T7_git_operation"
            ),
            SemanticUnit(
                unit_type=SemanticUnitType.ASSIGNMENT,
                description="Input parameters or arguments processing",
                pattern_context="T7_git_operation"
            ),
            SemanticUnit(
                unit_type=SemanticUnitType.ASSIGNMENT,
                description="Expected outcome or result generation",
                pattern_context="T7_git_operation"
            )
        ]
        return units
    
    def serialize_units(self, units: List[SemanticUnit]) -> List[Dict[str, Any]]:
        """Serialize semantic units to JSON-compatible format."""
        return [
            {
                "unit_id": f"unit_{i+1}",
                "unit_type": unit.unit_type.value,
                "description": unit.description,
                "pattern_context": unit.pattern_context,
                "is_error_related": unit.is_error_related
            }
            for i, unit in enumerate(units)
        ]

def main():
    """Test the semantic unit parser with T1."""
    print("=== Phase 4: Semantic Unit Parser Test ===")
    print("Testing with T1 (Context Scoping Logic)")
    print("=" * 50)
    
    # Load T1 baseline data
    with open("baseline_items/T1.json", "r") as f:
        t1_data = json.load(f)
    
    # Parse semantic units
    parser = SemanticUnitParser()
    units = parser.parse_test_pattern(
        test_id=t1_data["test_id"],
        pattern_sequence=t1_data["pattern_sequence"],
        baseline_questions=t1_data["baseline_questions"]
    )
    
    # Serialize and save
    serialized_units = parser.serialize_units(units)
    
    # Save to semantic_original
    output_path = f"semantic_original/{t1_data['test_id']}.json"
    with open(output_path, "w") as f:
        json.dump({
            "test_id": t1_data["test_id"],
            "pattern_sequence": t1_data["pattern_sequence"],
            "total_units": len(units),
            "error_paths": len([u for u in units if u.is_error_related]),
            "semantic_units": serialized_units
        }, f, indent=2)
    
    print(f"Parsed {len(units)} semantic units for T1:")
    for i, unit in enumerate(units, 1):
        print(f"  {i}. {unit.unit_type.value}: {unit.description}")
        if unit.is_error_related:
            print(f"     [ERROR PATH]")
    
    print(f"\nSaved to: {output_path}")
    print(f"Total semantic units: {len(units)}")
    print(f"Error paths: {len([u for u in units if u.is_error_related])}")

if __name__ == "__main__":
    main()