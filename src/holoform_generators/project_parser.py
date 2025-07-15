import os
import ast
from .main_generator import generate_holoform_from_code_string

import hashlib

CACHE_FILE = ".holoform_cache.json"

def parse_project(project_path):
    """
    Parses all Python files in a project directory and returns a list of Holoforms.
    """
    holoforms = []
    cache = _load_cache()

    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                file_hash = _get_file_hash(filepath)

                if filepath in cache and cache[filepath] == file_hash:
                    continue

                with open(filepath, 'r') as f:
                    source_code = f.read()

                try:
                    parsed_ast = ast.parse(source_code)
                    for node in parsed_ast.body:
                        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                            holoform = generate_holoform_from_code_string(source_code, target_name=node.name)
                            if holoform:
                                holoforms.append(holoform)
                except SyntaxError as e:
                    print(f"ERROR parsing {filepath}: {e}")

                cache[filepath] = file_hash

    _save_cache(cache)

    call_graph = _build_call_graph(holoforms)
    return holoforms, call_graph

def _load_cache():
    """
    Loads the file hash cache from disk.
    """
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            return json.load(f)
    else:
        return {}

def _save_cache(cache):
    """
    Saves the file hash cache to disk.
    """
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f)

def _get_file_hash(filepath):
    """
    Calculates the SHA256 hash of a file.
    """
    with open(filepath, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

def _build_call_graph(holoforms):
    """
    Builds a call graph from a list of Holoforms.
    """
    call_graph = {}
    for holoform in holoforms:
        if holoform.get("holoform_type") == "function":
            caller_id = holoform.get("id")
            if caller_id not in call_graph:
                call_graph[caller_id] = []

            for op in holoform.get("operations", []):
                if op.get("op_type") in ["function_call", "constructor_call"]:
                    callee_id = f"{op.get('target_function_name')}_auto_v1"
                    call_graph[caller_id].append(callee_id)

    return call_graph
