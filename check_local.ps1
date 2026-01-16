$ErrorActionPreference = "Stop"
Write-Host "🚀 Starting Local Quality Check (Backend Only)..." -ForegroundColor Cyan

# 1. Backend: Ruff
Write-Host "`n🔍 Checking Backend Style (Ruff)..." -ForegroundColor Yellow
try {
    ruff check backend/ --fix
    if ($LASTEXITCODE -ne 0) { throw "Ruff found errors" }
    Write-Host "✅ Ruff passed!" -ForegroundColor Green
} catch {
    Write-Host "❌ Ruff failed!" -ForegroundColor Red
    exit 1
}

# 2. Backend: Mypy
Write-Host "`n🧠 Checking Backend Types (Mypy)..." -ForegroundColor Yellow
try {
    mypy backend/
    if ($LASTEXITCODE -ne 0) { throw "Mypy found errors" }
    Write-Host "✅ Mypy passed!" -ForegroundColor Green
} catch {
    Write-Host "❌ Mypy failed!" -ForegroundColor Red
    exit 1
}

Write-Host "`n🎉 BACKEND CHECKS PASSED! You are ready to push." -ForegroundColor Cyan