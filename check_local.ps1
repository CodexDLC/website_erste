Write-Host "🚀 Starting Local Quality Check (Backend Only)..." -ForegroundColor Cyan

# 1. Backend: Ruff
Write-Host "`n🔍 Checking Backend Style (Ruff)..." -ForegroundColor Yellow
ruff check backend/ --fix
if ($LASTEXITCODE -ne 0) { Write-Host "❌ Ruff failed!" -ForegroundColor Red; exit 1 }
Write-Host "✅ Ruff passed!" -ForegroundColor Green

# 2. Backend: Mypy
Write-Host "`n🧠 Checking Backend Types (Mypy)..." -ForegroundColor Yellow
mypy backend/
if ($LASTEXITCODE -ne 0) { Write-Host "❌ Mypy failed!" -ForegroundColor Red; exit 1 }
Write-Host "✅ Mypy passed!" -ForegroundColor Green

Write-Host "`n🎉 BACKEND CHECKS PASSED! You are ready to push." -ForegroundColor Cyan