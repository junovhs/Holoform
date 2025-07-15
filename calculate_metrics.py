import os
import json
from src.holoform_generators.main_generator import generate_holoform_from_code_string
from src.holoform_generators.metrics import calculate_semantic_compression_ratio, calculate_semantic_fidelity_score

def calculate_metrics_for_file(filepath):
    """
    Calculates the metrics for a single Python file.
    """
    with open(filepath, 'r') as f:
        source_code = f.read()

    holoform = generate_holoform_from_code_string(source_code)

    if holoform:
        scr = calculate_semantic_compression_ratio(source_code, holoform)
        sfs = calculate_semantic_fidelity_score(source_code, holoform)
        return {"scr": scr, "sfs": sfs}
    else:
        return None

def main():
    """
    Calculates the metrics for all Python files in the `benchmark` directory.
    """
    benchmark_dir = "benchmark"
    if not os.path.exists(benchmark_dir):
        print(f"Benchmark directory not found: {benchmark_dir}")
        return

    results = {}
    for filename in os.listdir(benchmark_dir):
        if filename.endswith(".py"):
            filepath = os.path.join(benchmark_dir, filename)
            metrics = calculate_metrics_for_file(filepath)
            if metrics:
                results[filename] = metrics

    print(json.dumps(results, indent=4))

if __name__ == "__main__":
    main()
