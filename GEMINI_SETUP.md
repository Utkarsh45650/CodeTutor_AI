# 🤖 Google Gemini Setup Guide for CodeTutor AI

## 🎯 Quick Setup for Google Gemini

Your CodeTutor AI project is now configured to use **Google Gemini AI** exclusively!

### 🔑 **Step 1: Get Your Google Gemini API Key**

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key (it will look like: `AIza...`)

### ⚙️ **Step 2: Configure Your Environment**

1. Open the `.env` file in the `backend` folder
2. Replace `your-google-api-key-here` with your actual API key:

```bash
# Environment Configuration for CodeTutor AI

# Flask Configuration
SECRET_KEY=your-secret-key-change-this-in-production
DEBUG=True

# Google Gemini AI Configuration
GOOGLE_API_KEY=AIzaSyC_your_actual_api_key_here
```

### 🚀 **Step 3: Start the Application**

**Backend:**
```bash
cd backend
python app.py
```

**Frontend:**
```bash
cd frontend
npm start
```

## 🎉 **What's Configured**

✅ **Google Gemini Pro** model integration  
✅ **AI-powered tutorial generation**  
✅ **Intelligent quiz creation**  
✅ **Comprehensive notes compilation**  
✅ **Fallback to static content** if API fails  

## 💰 **Cost Information**

Google Gemini pricing (as of 2024):
- **Free tier**: 60 requests per minute
- **Paid tier**: ~$0.002 per 1K tokens (very affordable!)

Estimated monthly cost for 100 active users: **~$10-30/month**

## 🧪 **Test Your Setup**

1. Start both backend and frontend
2. Register/Login to the application
3. Navigate to any tutorial topic
4. Check if content is AI-generated (look for detailed, contextual explanations)
5. Take a quiz to see AI-generated questions

## 🔧 **Troubleshooting**

### **"Import google.generativeai could not be resolved"**
- Dependencies are installed correctly, this warning can be ignored

### **"AI API Error" messages in console**
- Check your `.env` file has the correct API key
- Verify your Google Cloud billing is set up (for paid tier)
- Check your API key permissions

### **Fallback content showing**
- This is normal behavior when AI API is unavailable
- Check your internet connection and API key

## 🎯 **Features Using Google Gemini**

1. **Tutorial Content**: Dynamic, context-aware programming tutorials
2. **Quiz Questions**: Adaptive questions based on difficulty level
3. **Comprehensive Notes**: Detailed study materials for each topic
4. **Code Examples**: Relevant code snippets and explanations

## 📊 **API Usage Monitoring**

Monitor your API usage at:
- [Google AI Studio Console](https://makersuite.google.com/)
- View quotas, usage, and billing information

## 🎨 **Customization Options**

Edit `backend/ai_service.py` to customize:
- **Temperature settings** (creativity level)
- **Model selection** (gemini-pro, gemini-pro-vision)
- **Token limits** and response formatting
- **Prompt engineering** for better responses

---

## 🎊 **You're All Set!**

Your CodeTutor AI now uses Google Gemini for:
- 🎓 **Smart tutorial generation**
- 🎯 **Adaptive quiz creation** 
- 📚 **Comprehensive note compilation**
- 💡 **Contextual programming guidance**

**Happy coding with AI-powered education!** 🚀
