# 🚀 CodeTutor AI Startup Script for Google Gemini
# This script starts both backend and frontend servers

Write-Host "🤖 Starting CodeTutor AI with Google Gemini..." -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Cyan

# Check if .env file exists
if (-not (Test-Path "backend\.env")) {
    Write-Host "❌ .env file not found!" -ForegroundColor Red
    Write-Host "📝 Please run: copy backend\.env.example backend\.env" -ForegroundColor Yellow
    Write-Host "   Then add your Google Gemini API key" -ForegroundColor Yellow
    exit 1
}

# Test Google Gemini setup
Write-Host "🧪 Testing Google Gemini setup..." -ForegroundColor Blue
Set-Location backend
$testResult = python test_gemini.py
Set-Location ..

if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Please configure your Google Gemini API key first" -ForegroundColor Yellow
    Write-Host "📖 See GEMINI_SETUP.md for detailed instructions" -ForegroundColor Cyan
    Read-Host "Press Enter to continue anyway or Ctrl+C to exit"
}

# Start backend in background
Write-Host "🔧 Starting Flask backend..." -ForegroundColor Green
Set-Location backend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python app.py" -WindowStyle Normal
Set-Location ..

# Wait a moment for backend to start
Start-Sleep -Seconds 3

# Start frontend
Write-Host "🎨 Starting React frontend..." -ForegroundColor Green
Set-Location frontend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "npm start" -WindowStyle Normal
Set-Location ..

Write-Host ""
Write-Host "🎉 CodeTutor AI is starting up!" -ForegroundColor Green
Write-Host ""
Write-Host "📱 Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "🔧 Backend: http://localhost:5000" -ForegroundColor Cyan
Write-Host ""
Write-Host "🤖 Google Gemini AI Features:" -ForegroundColor Yellow
Write-Host "   • Smart tutorial generation" -ForegroundColor White
Write-Host "   • Adaptive quiz questions" -ForegroundColor White
Write-Host "   • Comprehensive study notes" -ForegroundColor White
Write-Host "   • Code examples and explanations" -ForegroundColor White
Write-Host ""
Write-Host "📖 Need help? Check GEMINI_SETUP.md" -ForegroundColor Cyan
