from flask import Blueprint, request, jsonify
import hashlib
import json
import jwt
import datetime
from functools import wraps

auth_bp = Blueprint('auth', __name__)

def load_users():
    try:
        with open('database/users.json', 'r') as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open('database/users.json', 'w') as f:
        json.dump(users, f, indent=2)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            # Remove 'Bearer ' prefix if present
            if token.startswith('Bearer '):
                token = token[7:]
            
            data = jwt.decode(token, 'your-secret-key-here', algorithms=['HS256'])
            current_user = data['username']
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400
    
    users = load_users()
    
    if username in users:
        return jsonify({'message': 'Username already exists'}), 400
    
    users[username] = hash_password(password)
    save_users(users)
    
    # Initialize user progress
    try:
        with open('database/progress.json', 'r') as f:
            progress = json.load(f)
    except:
        progress = {}
    
    progress[username] = {
        'C': {'completed_topics': [], 'quiz_scores': {}},
        'C++': {'completed_topics': [], 'quiz_scores': {}},
        'C#': {'completed_topics': [], 'quiz_scores': {}},
        'Java': {'completed_topics': [], 'quiz_scores': {}},
        'Python': {'completed_topics': [], 'quiz_scores': {}}
    }
    
    with open('database/progress.json', 'w') as f:
        json.dump(progress, f, indent=2)
    
    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400
    
    users = load_users()
    
    if username not in users or users[username] != hash_password(password):
        return jsonify({'message': 'Invalid credentials'}), 401
    
    token = jwt.encode({
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, 'your-secret-key-here', algorithm='HS256')
    
    return jsonify({
        'token': token,
        'username': username,
        'message': 'Login successful'
    }), 200

@auth_bp.route('/user/progress', methods=['GET'])
@token_required
def get_progress(current_user):
    try:
        with open('database/progress.json', 'r') as f:
            progress = json.load(f)
        return jsonify(progress.get(current_user, {})), 200
    except:
        return jsonify({}), 200

@auth_bp.route('/user/progress', methods=['POST'])
@token_required
def update_progress(current_user):
    data = request.get_json()
    
    try:
        with open('database/progress.json', 'r') as f:
            progress = json.load(f)
    except:
        progress = {}
    
    if current_user not in progress:
        progress[current_user] = {
            'C': {'completed_topics': [], 'quiz_scores': {}},
            'C++': {'completed_topics': [], 'quiz_scores': {}},
            'C#': {'completed_topics': [], 'quiz_scores': {}},
            'Java': {'completed_topics': [], 'quiz_scores': {}},
            'Python': {'completed_topics': [], 'quiz_scores': {}}
        }
    
    language = data.get('language')
    topic = data.get('topic')
    quiz_score = data.get('quiz_score')
    
    if language and topic:
        if topic not in progress[current_user][language]['completed_topics']:
            progress[current_user][language]['completed_topics'].append(topic)
        
        if quiz_score is not None:
            progress[current_user][language]['quiz_scores'][topic] = quiz_score
    
    with open('database/progress.json', 'w') as f:
        json.dump(progress, f, indent=2)
    
    return jsonify({'message': 'Progress updated successfully'}), 200
