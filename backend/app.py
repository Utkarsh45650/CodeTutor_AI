from flask import Flask, request, jsonify
from flask_cors import CORS
from auth import auth_bp, token_required
from tutor import tutor_bp
from quiz import quiz_bp
from compiler import compiler_bp
from progress import progress_bp
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
CORS(app, origins=os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(','))

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(tutor_bp, url_prefix='/api')
app.register_blueprint(quiz_bp, url_prefix='/api')
app.register_blueprint(compiler_bp, url_prefix='/api')
app.register_blueprint(progress_bp, url_prefix='/api')

@app.route('/')
def home():
    return jsonify({"message": "CodeTutor AI Backend API"})

@app.route('/api/health')
def health_check():
    return jsonify({"status": "healthy"})

@app.route('/api/test-ai')
def test_ai():
    """Test endpoint to verify AI integration without authentication"""
    from ai_service import get_ai_service
    
    try:
        ai = get_ai_service()
        if ai.model is None:
            return jsonify({
                "status": "fallback",
                "message": "AI API not configured, using fallback content",
                "api_configured": False
            })
        
        # Test AI generation
        test_content = ai.generate_tutorial_content("Python", "Variables")
        
        return jsonify({
            "status": "success",
            "message": "AI integration working properly",
            "api_configured": True,
            "content_segments": len(test_content.get('content', [])),
            "checkpoints": len(test_content.get('checkpoints', [])),
            "sample_content": test_content.get('content', [''])[0][:100] + "..." if test_content.get('content') else "None"
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"AI integration error: {str(e)}",
            "api_configured": False
        })

if __name__ == '__main__':
    # Ensure database directory exists
    os.makedirs('database', exist_ok=True)
    
    # Initialize database files if they don't exist
    if not os.path.exists('database/users.json'):
        with open('database/users.json', 'w') as f:
            f.write('{}')
    
    if not os.path.exists('database/progress.json'):
        with open('database/progress.json', 'w') as f:
            f.write('{}')
    
    app.run(debug=True, port=5000)
