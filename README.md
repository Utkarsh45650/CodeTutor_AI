# CodeTutor AI

CodeTutor AI is an interactive educational platform designed to teach programming languages (C, C++, C#, Java, Python) through an AI-powered tutor and comprehensive quiz system. The platform features personalized learning paths, progress tracking, and an integrated compiler for hands-on coding challenges.

## 🌟 Features

### 🤖 AI-Powered Content Generation
- **Dynamic tutorial creation** using Google Gemini AI
- **Intelligent quiz generation** with context-aware questions
- **Comprehensive note compilation** for each programming topic
- **Fallback to curated content** when AI services are unavailable

### 🔐 User Authentication
- Complete registration and login system
- Secure user sessions with JWT tokens
- User progress tracking and persistence

### 🎓 AI Tutor Interface
- Interactive step-by-step learning powered by AI
- Checkpoint questions for understanding verification
- Sequential topic progression with AI-generated content
- Comprehensive notes automatically generated for each topic

### 🎯 Quiz System
- **AI-generated quiz questions** tailored to your learning progress
- Four difficulty levels: Easy, Medium, Hard, Nightmare
- Multiple question types: MCQ, Coding, Debugging
- Timer-based quizzes with auto-submission
- Detailed results with AI-powered explanations
- Custom quiz generator for completed topics

### 💻 Integrated Compiler
- Support for C, C++, C#, Java, and Python
- Real-time code execution
- Error handling and output display
- Secure sandboxed execution environment

### 🎨 Modern UI/UX
- Light and Dark theme support
- Responsive design for all devices
- Clean, intuitive interface
- Progress visualization

## 🛠️ Tech Stack

### Frontend
- **React.js** - UI framework
- **React Router DOM** - Navigation
- **CSS Modules** - Component-level styling
- **Context API** - State management

### Backend
- **Flask** - Python web framework
- **Google Gemini AI** - Advanced AI content generation
- **JWT** - Authentication tokens
- **JSON** - File-based database
- **Subprocess** - Code compilation and execution

### Styling
- **CSS Variables** - Theme management
- **Responsive Grid** - Layout system
- **CSS Modules** - Scoped styling

## 📁 Project Structure

```
AI_tutor/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── auth.py               # Authentication routes
│   ├── tutor.py              # Tutorial content routes
│   ├── quiz.py               # Quiz generation and submission
│   ├── compiler.py           # Code execution service
│   ├── ai_service.py         # AI integration service
│   ├── database/
│   │   ├── users.json        # User credentials
│   │   └── progress.json     # User progress data
│   ├── requirements.txt      # Python dependencies
│   ├── ai_requirements.txt   # AI provider packages
│   └── .env.example          # Environment variables template
├── frontend/
│   ├── public/
│   │   └── index.html        # HTML template
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── context/          # React contexts
│   │   ├── utils/            # Utility functions
│   │   ├── App.js            # Main app component
│   │   └── index.js          # App entry point
│   └── package.json          # Node.js dependencies
├── setup_ai.ps1             # Windows AI setup script
├── setup_ai.sh              # Linux/Mac AI setup script
├── AI_INTEGRATION_GUIDE.md  # Detailed AI setup guide
└── README.md                 # Project documentation
```

## 🤖 Google Gemini AI Setup

### 🚀 Quick Setup

1. **Get your Google Gemini API key:**
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create API key and copy it

2. **Configure environment:**
   ```bash
   cd backend
   copy .env.example .env  # Windows
   ```
   
   Edit `.env` file:
   ```bash
   GOOGLE_API_KEY=AIzaSyC_your_actual_api_key_here
   ```

3. **Start the application:**
   ```bash
   .\start_app.ps1  # Windows
   ```

📖 **For detailed setup instructions, see [GEMINI_SETUP.md](GEMINI_SETUP.md)**

## 🚀 Setup and Installation

### Prerequisites
- **Node.js** (v14 or higher)
- **Python** (v3.8 or higher)
- **Git**
- **AI API Key** (Google Gemini)

### Backend Setup

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install google-generativeai python-dotenv  # For Google Gemini AI
   ```

5. **Configure Google Gemini (copy from setup above):**
   ```bash
   copy .env.example .env  # Add your Google API key
   ```

6. **Run the Flask server:**
   ```bash
   python app.py
   ```

   The backend will be available at `http://localhost:5000`

### Frontend Setup

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```

   The frontend will be available at `http://localhost:3000`

### Compiler Setup (Optional)

For full code execution functionality, install the following compilers:

- **C/C++:** GCC or Clang
- **Java:** OpenJDK or Oracle JDK
- **C#:** .NET SDK
- **Python:** Already included

## 📚 API Endpoints

### Authentication
- `POST /api/register` - User registration
- `POST /api/login` - User login
- `GET /api/user/progress` - Get user progress (protected)
- `POST /api/user/progress` - Update user progress (protected)

### Tutorial Content
- `GET /api/tutor/content` - Get tutorial content for a topic (protected)
- `GET /api/tutor/topics` - Get available topics for a language (protected)
- `GET /api/tutor/notes` - Get comprehensive notes for a topic (protected)

### Quiz System
- `POST /api/quiz/generate` - Generate a quiz for a topic (protected)
- `POST /api/quiz/submit` - Submit quiz answers (protected)
- `POST /api/quiz/custom` - Generate custom quiz from multiple topics (protected)

### Code Execution
- `POST /api/run_code` - Execute code in specified language (protected)

## 🎮 Usage Guide

### Getting Started
1. **Register** a new account or **login** with existing credentials
2. **Select a programming language** from the dashboard
3. **Start learning** with the AI tutor for any topic
4. **Take quizzes** to test your understanding
5. **Track your progress** on the dashboard

### Learning Flow
1. **Tutorial** - Learn concepts step by step with the AI tutor
2. **Notes** - Review comprehensive notes for the topic
3. **Quiz** - Test your knowledge with interactive quizzes
4. **Progress** - See your advancement and unlock new features

### Advanced Features
- **Custom Quiz** - Available after completing 4 topics in a language
- **Code Compiler** - Practice coding directly in the browser
- **Progress Tracking** - Monitor your learning journey
- **Theme Switching** - Choose between light and dark modes

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the backend directory:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
```

### Database Configuration
The application uses JSON files for data storage:
- `backend/database/users.json` - User credentials
- `backend/database/progress.json` - User progress data

### Theme Customization
Modify CSS variables in `frontend/src/index.css` to customize the theme colors.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support, email support@codetutor-ai.com or create an issue in the GitHub repository.

## 🎯 Future Enhancements

- Integration with real AI/LLM APIs for dynamic content generation
- More programming languages support
- Collaborative learning features
- Advanced analytics and reporting
- Mobile app development
- Cloud deployment with scalable infrastructure

---

**CodeTutor AI** - Learn programming the smart way! 🚀
