# Weekend Hacker Holoform Demo Runner

Write-Host "🧬 Holoform Weekend Demo" -ForegroundColor Cyan
Write-Host "=======================" -ForegroundColor Cyan

# W-1: Generate Holoforms
Write-Host "Step 1: Generating Holoforms..." -ForegroundColor Yellow
python -c "import subprocess, json; result = subprocess.run(['python', 'holoform.py', 'examples/sample.py'], capture_output=True, text=True); data = json.loads(result.stdout); json.dump(data, open('holoforms.json', 'w'), indent=2)"

# W-2: Run evaluation
Write-Host "Step 2: Running evaluation..." -ForegroundColor Yellow
python eval.py examples/sample.py holoforms.json

# W-3: Show compression
Write-Host "Step 3: Compression demo..." -ForegroundColor Yellow
python symbolic_chain.py holoforms.json

Write-Host "✅ Demo complete!" -ForegroundColor Green