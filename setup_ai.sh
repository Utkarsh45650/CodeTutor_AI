#!/bin/bash

# 🚀 CodeTutor AI Setup Script
# This script automates the setup process for AI integration

echo "🤖 CodeTutor AI - AI Integration Setup"
echo "======================================"

# Function to prompt for user choice
ask_provider() {
    echo ""
    echo "Which AI provider would you like to use?"
    echo "1) OpenAI GPT-4 (Recommended)"
    echo "2) Anthropic Claude"
    echo "3) Google Gemini"
    echo "4) Local Ollama"
    echo ""
    read -p "Enter your choice (1-4): " choice
    
    case $choice in
        1) PROVIDER="openai" ;;
        2) PROVIDER="anthropic" ;;
        3) PROVIDER="google" ;;
        4) PROVIDER="ollama" ;;
        *) echo "Invalid choice. Using OpenAI as default."; PROVIDER="openai" ;;
    esac
}

# Function to install dependencies
install_deps() {
    echo ""
    echo "📦 Installing dependencies for $PROVIDER..."
    
    cd backend
    
    # Install base requirements
    echo "Installing base requirements..."
    pip install -r requirements.txt
    
    # Install AI provider specific packages
    case $PROVIDER in
        "openai")
            pip install openai==1.3.0 python-dotenv==1.0.0
            ;;
        "anthropic")
            pip install anthropic==0.8.0 python-dotenv==1.0.0
            ;;
        "google")
            pip install google-generativeai==0.3.0 python-dotenv==1.0.0
            ;;
        "ollama")
            pip install ollama-python==0.1.7 python-dotenv==1.0.0
            echo "Note: Make sure to install Ollama separately from https://ollama.ai/"
            ;;
    esac
    
    cd ..
}

# Function to setup environment file
setup_env() {
    echo ""
    echo "⚙️ Setting up environment variables..."
    
    cd backend
    
    # Copy example env file
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "Created .env file from .env.example"
    else
        # Create basic .env file
        cat > .env << EOF
# AI Provider Configuration
OPENAI_API_KEY=your-openai-api-key-here
ANTHROPIC_API_KEY=your-anthropic-api-key-here
GOOGLE_API_KEY=your-google-api-key-here

# Application Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True
EOF
        echo "Created .env file with default template"
    fi
    
    # Add .env to .gitignore if not already there
    if ! grep -q ".env" .gitignore 2>/dev/null; then
        echo ".env" >> .gitignore
        echo "Added .env to .gitignore"
    fi
    
    cd ..
}

# Function to prompt for API key
get_api_key() {
    echo ""
    case $PROVIDER in
        "openai")
            echo "🔑 Please get your OpenAI API key:"
            echo "1. Go to https://platform.openai.com/"
            echo "2. Create account or sign in"
            echo "3. Go to API Keys section"
            echo "4. Create new secret key"
            echo ""
            read -p "Enter your OpenAI API key (starts with sk-): " api_key
            sed -i "s/your-openai-api-key-here/$api_key/" backend/.env
            ;;
        "anthropic")
            echo "🔑 Please get your Anthropic API key:"
            echo "1. Go to https://console.anthropic.com/"
            echo "2. Create account and get API access"
            echo "3. Generate API key"
            echo ""
            read -p "Enter your Anthropic API key (starts with sk-ant-): " api_key
            sed -i "s/your-anthropic-api-key-here/$api_key/" backend/.env
            ;;
        "google")
            echo "🔑 Please get your Google API key:"
            echo "1. Go to https://makersuite.google.com/app/apikey"
            echo "2. Create API key"
            echo ""
            read -p "Enter your Google API key: " api_key
            sed -i "s/your-google-api-key-here/$api_key/" backend/.env
            ;;
        "ollama")
            echo "🏠 Using local Ollama - no API key needed"
            echo "Make sure Ollama is installed and running"
            ;;
    esac
}

# Function to install frontend dependencies
setup_frontend() {
    echo ""
    echo "📱 Setting up frontend..."
    
    cd frontend
    
    if [ ! -d "node_modules" ]; then
        echo "Installing npm dependencies..."
        npm install
    else
        echo "Frontend dependencies already installed"
    fi
    
    cd ..
}

# Function to test the setup
test_setup() {
    echo ""
    echo "🧪 Testing the setup..."
    
    # Test backend
    echo "Testing backend..."
    cd backend
    python -c "
import os
from dotenv import load_dotenv
load_dotenv()

print('✅ Python environment OK')

try:
    if '$PROVIDER' == 'openai':
        import openai
        print('✅ OpenAI package imported')
    elif '$PROVIDER' == 'anthropic':
        import anthropic
        print('✅ Anthropic package imported')
    elif '$PROVIDER' == 'google':
        import google.generativeai
        print('✅ Google AI package imported')
    elif '$PROVIDER' == 'ollama':
        import ollama
        print('✅ Ollama package imported')
except ImportError as e:
    print(f'❌ Import error: {e}')

# Check environment variables
api_key = os.getenv('${PROVIDER^^}_API_KEY')
if api_key and api_key != 'your-${PROVIDER}-api-key-here':
    print('✅ API key configured')
else:
    print('⚠️  API key not configured or still using placeholder')
"
    cd ..
}

# Main execution
main() {
    ask_provider
    install_deps
    setup_env
    
    if [ "$PROVIDER" != "ollama" ]; then
        get_api_key
    fi
    
    setup_frontend
    test_setup
    
    echo ""
    echo "🎉 Setup complete!"
    echo ""
    echo "Next steps:"
    echo "1. cd backend && python app.py (to start backend)"
    echo "2. cd frontend && npm start (to start frontend)"
    echo ""
    echo "📖 For detailed information, see AI_INTEGRATION_GUIDE.md"
}

# Run main function
main
