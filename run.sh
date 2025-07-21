#!/bin/bash
# Weekend Hacker Holoform Demo Runner

echo "🧬 Holoform Weekend Demo"
echo "======================="

# W-1: Generate Holoforms
echo "Step 1: Generating Holoforms..."
python holoform.py examples/sample.py > holoforms.json

# W-2: Run evaluation
echo "Step 2: Running evaluation..."
python eval.py examples/sample.py holoforms.json

# W-3: Show compression
echo "Step 3: Compression demo..."
python symbolic_chain.py holoforms.json

echo "✅ Demo complete!"