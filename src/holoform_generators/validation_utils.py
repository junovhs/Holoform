# AIResearchProject/src/holoform_generators/validation_utils.py
import json

def compare_holoforms(generated, expected, details_to_check=None):
    """Compares key fields of two Holoform dicts. Returns True if all checked fields match."""
    if not generated or not expected: return False
    
    passed = True
    
    # Default fields to check for all Holoforms
    common_fields = ["id", "description", "input_parameters", "output_variable_name"]
    if details_to_check is None:
        details_to_check = {field: True for field in common_fields}
        details_to_check["operations_structure"] = True # Default to check ops structure

    if details_to_check.get("id"):
        gen_id_base = generated.get("id", "").split('_auto_v1')[0]
        exp_id_base = expected.get("id", "").split('_auto_v1')[0]
        if gen_id_base != exp_id_base:
            print(f"  ID Mismatch: Gen='{generated.get('id')}', Exp base='{expected.get('id')}' ❌")
            passed = False

    if details_to_check.get("description"):
        # Normalize descriptions by stripping leading/trailing whitespace from each line and then the whole block
        # This aims to make comparison robust to slight original formatting differences preserved by clean=False
        norm_gen_desc = "\n".join([l.strip() for l in generated.get("description", "").splitlines()]).strip()
        norm_exp_desc = "\n".join([l.strip() for l in expected.get("description", "").splitlines()]).strip()
        if norm_gen_desc != norm_exp_desc:
            print(f"  Description Mismatch: ❌")
            print(f"    Generated (Norm): '''{norm_gen_desc}'''")
            print(f"    Expected (Norm):  '''{norm_exp_desc}'''")
            passed = False

    if details_to_check.get("input_parameters"):
        if generated.get("input_parameters") != expected.get("input_parameters"):
            print(f"  Input Params Mismatch: Gen={generated.get('input_parameters')}, Exp={expected.get('input_parameters')} ❌")
            passed = False

    if details_to_check.get("output_variable_name"):
        if generated.get("output_variable_name") != expected.get("output_variable_name"):
            print(f"  Output Var Name Mismatch: Gen={generated.get('output_variable_name')}, Exp={expected.get('output_variable_name')} ❌")
            passed = False

    if details_to_check.get("operations_structure"):
        gen_ops = generated.get("operations", [])
        exp_ops_check = expected.get("operations", []) # Expected ops often has only specific fields for checking
        if len(gen_ops) == len(exp_ops_check):
            for i, exp_op_subset in enumerate(exp_ops_check):
                gen_op_full = gen_ops[i]
                op_match = True
                for key, exp_val in exp_op_subset.items():
                    if key == "loop_body_operations": # Recursive check for nested operations
                        if not compare_nested_ops(gen_op_full.get(key, []), exp_val):
                            op_match = False; break
                    elif gen_op_full.get(key) != exp_val:
                        op_match = False
                        print(f"    Op[{i}] Mismatch on '{key}': Gen='{gen_op_full.get(key)}', Exp='{exp_val}' ❌")
                        break 
                if not op_match: passed = False; break # Stop checking ops for this scenario if one mismatch
        else:
            print(f"  Operations Count Mismatch: Gen={len(gen_ops)}, Exp={len(exp_ops_check)} ❌")
            # print("DEBUG Gen Ops:", json.dumps(gen_ops, indent=2))
            # print("DEBUG Exp Ops Check:", json.dumps(exp_ops_check, indent=2))
            passed = False
            
    return passed

def compare_nested_ops(gen_nested_ops, exp_nested_ops_check):
    if len(gen_nested_ops) != len(exp_nested_ops_check): return False
    for i, exp_op_subset in enumerate(exp_nested_ops_check):
        gen_op_full = gen_nested_ops[i]
        for key, exp_val in exp_op_subset.items():
            if gen_op_full.get(key) != exp_val: return False
    return True

# Main execution test harness will be in a separate test file or __main__ of main_generator.py
# This file is just for utilities.
