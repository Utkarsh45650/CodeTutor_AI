# 🚀 CodeTutor AI Setup Script for Windows
# This script automates the setup process for AI integration

Write-Host "🤖 CodeTutor AI - AI Integration Setup" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan

# Function to prompt for user choice
function Ask-Provider {
    Write-Host ""
    Write-Host "Which AI provider would you like to use?" -ForegroundColor Yellow
    Write-Host "1) OpenAI GPT-4 (Recommended)" -ForegroundColor Green
    Write-Host "2) Anthropic Claude" -ForegroundColor Green
    Write-Host "3) Google Gemini" -ForegroundColor Green
    Write-Host "4) Local Ollama" -ForegroundColor Green
    Write-Host ""
    
    $choice = Read-Host "Enter your choice (1-4)"
    
    switch ($choice) {
        "1" { return "openai" }
        "2" { return "anthropic" }
        "3" { return "google" }
        "4" { return "ollama" }
        default { 
            Write-Host "Invalid choice. Using OpenAI as default." -ForegroundColor Yellow
            return "openai" 
        }
    }
}

# Function to install dependencies
function Install-Dependencies($provider) {
    Write-Host ""
    Write-Host "📦 Installing dependencies for $provider..." -ForegroundColor Blue
    
    Set-Location backend
    
    # Install base requirements
    Write-Host "Installing base requirements..." -ForegroundColor Green
    pip install -r requirements.txt
    
    # Install AI provider specific packages
    switch ($provider) {
        "openai" {
            pip install openai==1.3.0 python-dotenv==1.0.0
        }
        "anthropic" {
            pip install anthropic==0.8.0 python-dotenv==1.0.0
        }
        "google" {
            pip install google-generativeai==0.3.0 python-dotenv==1.0.0
        }
        "ollama" {
            pip install ollama-python==0.1.7 python-dotenv==1.0.0
            Write-Host "Note: Make sure to install Ollama separately from https://ollama.ai/" -ForegroundColor Yellow
        }
    }
    
    Set-Location ..
}

# Function to setup environment file
function Setup-Environment {
    Write-Host ""
    Write-Host "⚙️ Setting up environment variables..." -ForegroundColor Blue
    
    Set-Location backend
    
    # Copy example env file
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host "Created .env file from .env.example" -ForegroundColor Green
    } else {
        # Create basic .env file
        $envContent = @"
# AI Provider Configuration
OPENAI_API_KEY=your-openai-api-key-here
ANTHROPIC_API_KEY=your-anthropic-api-key-here
GOOGLE_API_KEY=your-google-api-key-here

# Application Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True
"@
        $envContent | Out-File -FilePath ".env" -Encoding UTF8
        Write-Host "Created .env file with default template" -ForegroundColor Green
    }
    
    # Add .env to .gitignore if not already there
    if (Test-Path ".gitignore") {
        $gitignoreContent = Get-Content ".gitignore" -ErrorAction SilentlyContinue
        if ($gitignoreContent -notcontains ".env") {
            Add-Content ".gitignore" ".env"
            Write-Host "Added .env to .gitignore" -ForegroundColor Green
        }
    } else {
        ".env" | Out-File -FilePath ".gitignore" -Encoding UTF8
        Write-Host "Created .gitignore and added .env" -ForegroundColor Green
    }
    
    Set-Location ..
}

# Function to prompt for API key
function Get-ApiKey($provider) {
    Write-Host ""
    switch ($provider) {
        "openai" {
            Write-Host "🔑 Please get your OpenAI API key:" -ForegroundColor Yellow
            Write-Host "1. Go to https://platform.openai.com/" -ForegroundColor White
            Write-Host "2. Create account or sign in" -ForegroundColor White
            Write-Host "3. Go to API Keys section" -ForegroundColor White
            Write-Host "4. Create new secret key" -ForegroundColor White
            Write-Host ""
            $apiKey = Read-Host "Enter your OpenAI API key (starts with sk-)"
            if ($apiKey) {
                (Get-Content "backend\.env") -replace "your-openai-api-key-here", $apiKey | Set-Content "backend\.env"
                Write-Host "✅ OpenAI API key configured" -ForegroundColor Green
            }
        }
        "anthropic" {
            Write-Host "🔑 Please get your Anthropic API key:" -ForegroundColor Yellow
            Write-Host "1. Go to https://console.anthropic.com/" -ForegroundColor White
            Write-Host "2. Create account and get API access" -ForegroundColor White
            Write-Host "3. Generate API key" -ForegroundColor White
            Write-Host ""
            $apiKey = Read-Host "Enter your Anthropic API key (starts with sk-ant-)"
            if ($apiKey) {
                (Get-Content "backend\.env") -replace "your-anthropic-api-key-here", $apiKey | Set-Content "backend\.env"
                Write-Host "✅ Anthropic API key configured" -ForegroundColor Green
            }
        }
        "google" {
            Write-Host "🔑 Please get your Google API key:" -ForegroundColor Yellow
            Write-Host "1. Go to https://makersuite.google.com/app/apikey" -ForegroundColor White
            Write-Host "2. Create API key" -ForegroundColor White
            Write-Host ""
            $apiKey = Read-Host "Enter your Google API key"
            if ($apiKey) {
                (Get-Content "backend\.env") -replace "your-google-api-key-here", $apiKey | Set-Content "backend\.env"
                Write-Host "✅ Google API key configured" -ForegroundColor Green
            }
        }
        "ollama" {
            Write-Host "🏠 Using local Ollama - no API key needed" -ForegroundColor Green
            Write-Host "Make sure Ollama is installed and running" -ForegroundColor Yellow
        }
    }
}

# Function to install frontend dependencies
function Setup-Frontend {
    Write-Host ""
    Write-Host "📱 Setting up frontend..." -ForegroundColor Blue
    
    Set-Location frontend
    
    if (-not (Test-Path "node_modules")) {
        Write-Host "Installing npm dependencies..." -ForegroundColor Green
        npm install
    } else {
        Write-Host "Frontend dependencies already installed" -ForegroundColor Green
    }
    
    Set-Location ..
}

# Function to test the setup
function Test-Setup($provider) {
    Write-Host ""
    Write-Host "🧪 Testing the setup..." -ForegroundColor Blue
    
    # Test backend
    Write-Host "Testing backend..." -ForegroundColor Green
    Set-Location backend
    
    $testScript = @"
import os
from dotenv import load_dotenv
load_dotenv()

print('✅ Python environment OK')

try:
    if '$provider' == 'openai':
        import openai
        print('✅ OpenAI package imported')
    elif '$provider' == 'anthropic':
        import anthropic
        print('✅ Anthropic package imported')
    elif '$provider' == 'google':
        import google.generativeai
        print('✅ Google AI package imported')
    elif '$provider' == 'ollama':
        import ollama
        print('✅ Ollama package imported')
except ImportError as e:
    print(f'❌ Import error: {e}')

# Check environment variables
api_key_name = '${provider}'.upper() + '_API_KEY'
api_key = os.getenv(api_key_name)
if api_key and not api_key.startswith('your-'):
    print('✅ API key configured')
else:
    print('⚠️  API key not configured or still using placeholder')
"@
    
    $testScript | python
    Set-Location ..
}

# Main execution
function Main {
    $provider = Ask-Provider
    Install-Dependencies $provider
    Setup-Environment
    
    if ($provider -ne "ollama") {
        Get-ApiKey $provider
    }
    
    Setup-Frontend
    Test-Setup $provider
    
    Write-Host ""
    Write-Host "🎉 Setup complete!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. cd backend; python app.py (to start backend)" -ForegroundColor White
    Write-Host "2. cd frontend; npm start (to start frontend)" -ForegroundColor White
    Write-Host ""
    Write-Host "📖 For detailed information, see AI_INTEGRATION_GUIDE.md" -ForegroundColor Cyan
}

# Run main function
Main
