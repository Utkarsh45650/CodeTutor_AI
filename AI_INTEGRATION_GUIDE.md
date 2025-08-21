# 🤖 AI API Integration Guide for CodeTutor AI

## 🎯 **Overview**

CodeTutor AI supports multiple AI providers for generating educational content. Choose the option that best fits your needs:

### **Recommended AI Providers:**

1. **🥇 OpenAI GPT-4** (Recommended)
   - Best quality for educational content
   - Great at following structured prompts
   - Cost: ~$0.03 per 1K tokens

2. **🥈 Anthropic Claude**
   - Excellent safety and reasoning
   - Good for structured educational content
   - Cost: ~$0.025 per 1K tokens

3. **🥉 Google Gemini**
   - Good performance, competitive pricing
   - Fast response times
   - Cost: ~$0.002 per 1K tokens

4. **🏠 Local Models (Ollama)**
   - Complete privacy (runs locally)
   - No API costs
   - Requires powerful hardware

## 🚀 **Quick Setup Instructions**

### **Step 1: Choose Your Provider and Get API Key**

#### **Option A: OpenAI (Recommended)**
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Create account or sign in
3. Go to API Keys section
4. Create new secret key
5. Copy the key (starts with `sk-...`)

#### **Option B: Anthropic Claude**
1. Go to [Anthropic Console](https://console.anthropic.com/)
2. Create account and get API access
3. Generate API key
4. Copy the key (starts with `sk-ant-...`)

#### **Option C: Google Gemini**
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create API key
3. Copy the key

#### **Option D: Local Models (Ollama)**
1. Install [Ollama](https://ollama.ai/)
2. Run: `ollama pull llama2` or `ollama pull codellama`
3. No API key needed

### **Step 2: Install Dependencies**

```bash
cd backend

# Install base requirements
pip install -r requirements.txt

# Install AI provider (choose one)

# For OpenAI:
pip install openai==1.3.0 python-dotenv==1.0.0

# For Anthropic:
pip install anthropic==0.8.0 python-dotenv==1.0.0

# For Google Gemini:
pip install google-generativeai==0.3.0 python-dotenv==1.0.0

# For Local Ollama:
pip install ollama-python==0.1.7 python-dotenv==1.0.0
```

### **Step 3: Configure Environment Variables**

1. **Copy the example environment file:**
   ```bash
   copy .env.example .env
   ```

2. **Edit `.env` file with your API key:**
   ```bash
   # For OpenAI
   OPENAI_API_KEY=sk-your-actual-api-key-here
   
   # For Anthropic
   ANTHROPIC_API_KEY=sk-ant-your-api-key-here
   
   # For Google
   GOOGLE_API_KEY=your-google-api-key-here
   
   # Other settings
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ```

3. **Add `.env` to `.gitignore`:**
   ```bash
   echo .env >> .gitignore
   ```

### **Step 4: Update AI Service (if using different provider)**

Edit `backend/ai_service.py` to use your preferred provider:

```python
# For Anthropic Claude
import anthropic

class AIService:
    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=os.getenv('ANTHROPIC_API_KEY')
        )
    
    def generate_tutorial_content(self, language: str, topic: str):
        response = self.client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )
        return json.loads(response.content[0].text)

# For Google Gemini
import google.generativeai as genai

class AIService:
    def __init__(self):
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        self.model = genai.GenerativeModel('gemini-pro')
    
    def generate_tutorial_content(self, language: str, topic: str):
        response = self.model.generate_content(prompt)
        return json.loads(response.text)

# For Local Ollama
import ollama

class AIService:
    def __init__(self):
        self.client = ollama.Client(host=os.getenv('OLLAMA_HOST', 'http://localhost:11434'))
    
    def generate_tutorial_content(self, language: str, topic: str):
        response = self.client.generate(
            model='llama2',  # or 'codellama'
            prompt=prompt
        )
        return json.loads(response['response'])
```

### **Step 5: Test the Integration**

1. **Start the backend:**
   ```bash
   cd backend
   python app.py
   ```

2. **Start the frontend:**
   ```bash
   cd frontend
   npm start
   ```

3. **Test AI features:**
   - Register/Login to the application
   - Try accessing a tutorial (should use AI-generated content)
   - Take a quiz (should use AI-generated questions)
   - Check browser console for any AI API errors

## 💰 **Cost Estimation**

### **Per User Session (estimated):**
- **Tutorial Content**: ~500-1000 tokens = $0.01-0.03
- **Quiz Generation**: ~800-1500 tokens = $0.02-0.05
- **Notes Generation**: ~1000-2000 tokens = $0.03-0.06

### **Monthly Costs (100 active users):**
- **OpenAI**: ~$50-150/month
- **Anthropic**: ~$40-120/month  
- **Google**: ~$10-30/month
- **Local Models**: Free (hardware cost)

## 🔧 **Advanced Configuration**

### **Rate Limiting**
Add rate limiting to prevent API abuse:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/tutor/content')
@limiter.limit("10 per minute")
@token_required
def get_tutor_content(current_user):
    # Your code here
```

### **Caching**
Add caching to reduce API calls:

```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@cache.memoize(timeout=3600)  # Cache for 1 hour
def generate_tutorial_content(language, topic):
    return ai_service.generate_tutorial_content(language, topic)
```

### **Fallback Strategy**
The current implementation already includes fallbacks:
1. Try AI API first
2. If API fails, use hardcoded content
3. Log errors for monitoring

## 🔒 **Security Best Practices**

1. **Never commit API keys to Git**
2. **Use environment variables**
3. **Implement rate limiting**
4. **Monitor API usage and costs**
5. **Validate all AI-generated content**
6. **Use HTTPS in production**

## 🐛 **Troubleshooting**

### **Common Issues:**

1. **"Import openai could not be resolved"**
   - Install: `pip install openai python-dotenv`

2. **"API key not found"**
   - Check `.env` file exists and has correct key
   - Restart the Flask server after adding keys

3. **"AI API Error: 401 Unauthorized"**
   - Verify API key is correct
   - Check if you have API credits/billing setup

4. **"Content generation failed"**
   - Check internet connection
   - Verify API service status
   - Check rate limits

5. **"Fallback content showing"**
   - This is normal when AI API is unavailable
   - Check logs for specific error messages

## 📊 **Monitoring and Analytics**

Add logging to track AI usage:

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_tutorial_content(self, language: str, topic: str):
    logger.info(f"Generating content for {language} - {topic}")
    try:
        # AI generation code
        logger.info("Content generated successfully")
    except Exception as e:
        logger.error(f"AI generation failed: {e}")
```

## 🎯 **Production Deployment**

For production deployment:

1. **Use production-grade API keys**
2. **Set up proper environment management**
3. **Implement monitoring and alerting**
4. **Use Redis for caching**
5. **Set up API usage dashboards**
6. **Implement graceful degradation**

---

## 📞 **Support**

If you encounter issues:
1. Check the troubleshooting section above
2. Review API provider documentation
3. Check application logs
4. Create an issue in the project repository

**Happy Coding! 🚀**
