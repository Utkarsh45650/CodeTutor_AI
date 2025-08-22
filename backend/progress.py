from flask import Blueprint, request, jsonify
from auth import token_required
import json
import os

progress_bp = Blueprint('progress', __name__)

# Define topic progression structure
TOPIC_PROGRESSION = {
    'Python': [
        {
            'level': 1,
            'topic': 'Variables and Data Types',
            'description': 'Learn about variables, numbers, strings, and basic data types',
            'prerequisites': []
        },
        {
            'level': 2,
            'topic': 'Control Structures',
            'description': 'Master if statements, loops, and conditional logic',
            'prerequisites': ['Variables and Data Types']
        },
        {
            'level': 3,
            'topic': 'Functions',
            'description': 'Create reusable code with functions and parameters',
            'prerequisites': ['Control Structures']
        },
        {
            'level': 4,
            'topic': 'Lists and Dictionaries',
            'description': 'Work with collections and data structures',
            'prerequisites': ['Functions']
        },
        {
            'level': 5,
            'topic': 'File Handling',
            'description': 'Read from and write to files',
            'prerequisites': ['Lists and Dictionaries']
        },
        {
            'level': 6,
            'topic': 'Object-Oriented Programming',
            'description': 'Classes, objects, inheritance, and encapsulation',
            'prerequisites': ['File Handling']
        }
    ],
    'Java': [
        {
            'level': 1,
            'topic': 'Variables and Data Types',
            'description': 'Learn Java syntax, variables, and primitive data types',
            'prerequisites': []
        },
        {
            'level': 2,
            'topic': 'Control Structures',
            'description': 'Master if-else, loops, and switch statements',
            'prerequisites': ['Variables and Data Types']
        },
        {
            'level': 3,
            'topic': 'Methods',
            'description': 'Create and use methods (functions) in Java',
            'prerequisites': ['Control Structures']
        },
        {
            'level': 4,
            'topic': 'Arrays and Collections',
            'description': 'Work with arrays, ArrayList, and other collections',
            'prerequisites': ['Methods']
        },
        {
            'level': 5,
            'topic': 'Object-Oriented Programming',
            'description': 'Classes, objects, inheritance, and polymorphism',
            'prerequisites': ['Arrays and Collections']
        },
        {
            'level': 6,
            'topic': 'Exception Handling',
            'description': 'Handle errors and exceptions gracefully',
            'prerequisites': ['Object-Oriented Programming']
        }
    ],
    'C': [
        {
            'level': 1,
            'topic': 'Variables and Data Types',
            'description': 'Learn C syntax, variables, and basic data types',
            'prerequisites': []
        },
        {
            'level': 2,
            'topic': 'Control Structures',
            'description': 'Master if-else, loops, and conditional statements',
            'prerequisites': ['Variables and Data Types']
        },
        {
            'level': 3,
            'topic': 'Functions',
            'description': 'Create and use functions in C',
            'prerequisites': ['Control Structures']
        },
        {
            'level': 4,
            'topic': 'Arrays and Strings',
            'description': 'Work with arrays and string manipulation',
            'prerequisites': ['Functions']
        },
        {
            'level': 5,
            'topic': 'Pointers',
            'description': 'Understand memory addresses and pointer operations',
            'prerequisites': ['Arrays and Strings']
        },
        {
            'level': 6,
            'topic': 'Structures and Unions',
            'description': 'Group related data using structures',
            'prerequisites': ['Pointers']
        }
    ],
    'JavaScript': [
        {
            'level': 1,
            'topic': 'Variables and Data Types',
            'description': 'Learn JavaScript variables, strings, numbers, and booleans',
            'prerequisites': []
        },
        {
            'level': 2,
            'topic': 'Control Structures',
            'description': 'Master if-else, loops, and conditional logic',
            'prerequisites': ['Variables and Data Types']
        },
        {
            'level': 3,
            'topic': 'Functions',
            'description': 'Create functions, arrow functions, and closures',
            'prerequisites': ['Control Structures']
        },
        {
            'level': 4,
            'topic': 'Arrays and Objects',
            'description': 'Work with arrays, objects, and JSON',
            'prerequisites': ['Functions']
        },
        {
            'level': 5,
            'topic': 'DOM Manipulation',
            'description': 'Interact with HTML elements and events',
            'prerequisites': ['Arrays and Objects']
        },
        {
            'level': 6,
            'topic': 'Asynchronous JavaScript',
            'description': 'Promises, async/await, and API calls',
            'prerequisites': ['DOM Manipulation']
        }
    ]
}

def load_user_progress():
    """Load user progress from JSON file"""
    try:
        with open('database/progress.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_user_progress(progress_data):
    """Save user progress to JSON file"""
    with open('database/progress.json', 'w') as f:
        json.dump(progress_data, f, indent=2)

@progress_bp.route('/topics/<language>')
@token_required
def get_topics_with_progress(current_user, language):
    """Get topics for a language with user progress and lock status"""
    if language not in TOPIC_PROGRESSION:
        return jsonify({'error': 'Language not supported'}), 400
    
    progress_data = load_user_progress()
    user_progress = progress_data.get(current_user, {}).get(language, {})
    
    topics_with_progress = []
    
    for topic_info in TOPIC_PROGRESSION[language]:
        topic_name = topic_info['topic']
        user_topic_progress = user_progress.get(topic_name, {})
        
        # Check if topic is unlocked
        is_unlocked = True
        for prereq in topic_info['prerequisites']:
            prereq_progress = user_progress.get(prereq, {})
            if not prereq_progress.get('completed', False):
                is_unlocked = False
                break
        
        topic_data = {
            'level': topic_info['level'],
            'topic': topic_name,
            'description': topic_info['description'],
            'prerequisites': topic_info['prerequisites'],
            'is_unlocked': is_unlocked,
            'completed': user_topic_progress.get('completed', False),
            'tutorial_completed': user_topic_progress.get('tutorial_completed', False),
            'quiz_attempts': user_topic_progress.get('quiz_attempts', 0),
            'best_quiz_score': user_topic_progress.get('best_quiz_score', 0),
            'last_accessed': user_topic_progress.get('last_accessed', None)
        }
        
        topics_with_progress.append(topic_data)
    
    return jsonify({
        'language': language,
        'topics': topics_with_progress,
        'total_completed': sum(1 for t in topics_with_progress if t['completed'])
    })

@progress_bp.route('/complete-tutorial', methods=['POST'])
@token_required
def complete_tutorial(current_user):
    """Mark a tutorial as completed"""
    data = request.get_json()
    language = data.get('language')
    topic = data.get('topic')
    
    if not language or not topic:
        return jsonify({'error': 'Language and topic are required'}), 400
    
    progress_data = load_user_progress()
    
    # Initialize user progress if not exists
    if current_user not in progress_data:
        progress_data[current_user] = {}
    
    if language not in progress_data[current_user]:
        progress_data[current_user][language] = {}
    
    if topic not in progress_data[current_user][language]:
        progress_data[current_user][language][topic] = {}
    
    # Mark tutorial as completed
    progress_data[current_user][language][topic]['tutorial_completed'] = True
    progress_data[current_user][language][topic]['last_accessed'] = str(json.dumps(None))  # Current timestamp
    
    save_user_progress(progress_data)
    
    return jsonify({'message': 'Tutorial completed successfully'})

@progress_bp.route('/complete-quiz', methods=['POST'])
@token_required
def complete_quiz(current_user):
    """Record quiz completion and score"""
    data = request.get_json()
    language = data.get('language')
    topic = data.get('topic')
    score = data.get('score', 0)
    
    if not language or not topic:
        return jsonify({'error': 'Language and topic are required'}), 400
    
    progress_data = load_user_progress()
    
    # Initialize user progress if not exists
    if current_user not in progress_data:
        progress_data[current_user] = {}
    
    if language not in progress_data[current_user]:
        progress_data[current_user][language] = {}
    
    if topic not in progress_data[current_user][language]:
        progress_data[current_user][language][topic] = {}
    
    topic_progress = progress_data[current_user][language][topic]
    
    # Update quiz progress
    topic_progress['quiz_attempts'] = topic_progress.get('quiz_attempts', 0) + 1
    topic_progress['best_quiz_score'] = max(topic_progress.get('best_quiz_score', 0), score)
    topic_progress['last_accessed'] = str(json.dumps(None))  # Current timestamp
    
    # Mark topic as completed if score is above threshold (e.g., 70%)
    if score >= 70:
        topic_progress['completed'] = True
    
    save_user_progress(progress_data)
    
    return jsonify({
        'message': 'Quiz completed successfully',
        'topic_completed': topic_progress.get('completed', False),
        'best_score': topic_progress['best_quiz_score']
    })
