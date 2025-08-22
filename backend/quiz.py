from flask import Blueprint, request, jsonify
from auth import token_required
from ai_service import get_ai_service
import random

quiz_bp = Blueprint('quiz', __name__)

# Simple in-memory cache for quiz questions (in production, use Redis or database)
quiz_cache = {}

def cleanup_old_cache_entries():
    """Remove cache entries older than 1 hour"""
    import time
    current_time = time.time()
    to_remove = []
    for quiz_id, data in quiz_cache.items():
        if current_time - data['timestamp'] > 3600:  # 1 hour
            to_remove.append(quiz_id)
    for quiz_id in to_remove:
        del quiz_cache[quiz_id]

@quiz_bp.route('/quiz/generate', methods=['POST'])
@token_required
def generate_quiz(current_user):
    # Clean up old cache entries periodically
    cleanup_old_cache_entries()
    
    data = request.get_json()
    language = data.get('language')
    topic = data.get('topic')
    difficulty = data.get('difficulty', 'Easy')
    num_questions = data.get('num_questions', 5)
    
    if not language or not topic:
        return jsonify({'error': 'Language and topic are required'}), 400
    
    # Validate difficulty
    valid_difficulties = ['Easy', 'Medium', 'Hard', 'Expert']
    if difficulty not in valid_difficulties:
        difficulty = 'Easy'
    
    print(f"Quiz generation requested: {language} - {topic} ({difficulty}) - {num_questions} questions")
    
    # Try AI service first with enhanced error handling
    try:
        print("Attempting AI quiz generation...")
        ai_questions = get_ai_service().generate_quiz_questions(language, topic, difficulty, num_questions)
        
        if ai_questions and len(ai_questions) > 0:
            print(f"AI generated {len(ai_questions)} questions successfully")
            
            # Generate unique quiz ID
            quiz_id = f"{language}_{topic}_{difficulty}_{random.randint(1000, 9999)}"
            
            # Store quiz questions in cache for later validation
            quiz_cache[quiz_id] = {
                'questions': ai_questions,
                'language': language,
                'topic': topic,
                'difficulty': difficulty,
                'timestamp': __import__('time').time()
            }
            
            # Format the response properly
            quiz_response = {
                'success': True,
                'quiz_id': quiz_id,
                'language': language,
                'topic': topic,
                'difficulty': difficulty,
                'questions': ai_questions,
                'total_questions': len(ai_questions),
                'time_limit': _calculate_time_limit(difficulty, len(ai_questions)),
                'source': 'ai',
                'instructions': _get_quiz_instructions(difficulty)
            }
            
            return jsonify(quiz_response), 200
        else:
            print("AI service returned empty result, falling back to hardcoded")
            raise Exception("AI service returned empty questions")
            
    except Exception as e:
        print(f"AI service failed, using fallback: {e}")
        # Fallback to hardcoded content
        fallback_questions = _get_fallback_quiz_questions(language, topic, difficulty, num_questions)
        
        # Generate unique quiz ID
        quiz_id = f"{language}_{topic}_{difficulty}_{random.randint(1000, 9999)}"
        
        # Store fallback questions in cache too
        quiz_cache[quiz_id] = {
            'questions': fallback_questions,
            'language': language,
            'topic': topic,
            'difficulty': difficulty,
            'timestamp': __import__('time').time()
        }
        
        quiz_response = {
            'success': True,
            'quiz_id': quiz_id,
            'language': language,
            'topic': topic,
            'difficulty': difficulty,
            'questions': fallback_questions,
            'total_questions': len(fallback_questions),
            'time_limit': _calculate_time_limit(difficulty, len(fallback_questions)),
            'source': 'fallback',
            'instructions': _get_quiz_instructions(difficulty),
            'warning': 'AI service unavailable, using sample questions'
        }
        
        return jsonify(quiz_response), 200

@quiz_bp.route('/quiz/submit', methods=['POST'])
@token_required
def submit_quiz(current_user):
    data = request.get_json()
    quiz_id = data.get('quiz_id')
    answers = data.get('answers', [])
    language = data.get('language')
    topic = data.get('topic')
    difficulty = data.get('difficulty')
    
    if not quiz_id or not answers:
        return jsonify({'error': 'Quiz ID and answers are required'}), 400
    
    # Calculate score and detailed results
    score = 0
    total_questions = len(answers)
    detailed_results = []
    
    print(f"Evaluating quiz: {quiz_id}")
    print(f"Received {total_questions} answers: {answers}")
    
    # Get quiz questions for validation (this is a simplified approach)
    try:
        # First try to get questions from cache
        if quiz_id in quiz_cache:
            print(f"Using cached questions for quiz {quiz_id}")
            quiz_questions = quiz_cache[quiz_id]['questions']
            # Clean up old cache entry
            del quiz_cache[quiz_id]
        else:
            print(f"Cache miss for quiz {quiz_id}, regenerating questions")
            # Fallback: re-generate the same quiz for validation (not ideal but works)
            quiz_questions = get_ai_service().generate_quiz_questions(language, topic, difficulty, total_questions)
        
        print(f"Using {len(quiz_questions)} questions for validation")
        
        for i, (user_answer, question) in enumerate(zip(answers, quiz_questions)):
            is_correct = False
            
            if question.get('type') == 'mcq':
                correct_answer = question.get('correct', 0)
                # Ensure both answers are the same type for comparison
                try:
                    user_answer_int = int(user_answer) if user_answer != '' else -1
                    is_correct = user_answer_int == correct_answer
                    print(f"Question {i+1}: User: {user_answer_int}, Correct: {correct_answer}, Match: {is_correct}")
                except (ValueError, TypeError):
                    print(f"Question {i+1}: Invalid user answer format: {user_answer}")
                    is_correct = False
            else:
                # For coding questions, this would need more sophisticated evaluation
                is_correct = True  # Simplified for now
            
            if is_correct:
                score += 1
            
            detailed_results.append({
                'question_number': i + 1,
                'question': question.get('question', ''),
                'user_answer': user_answer,
                'correct_answer': question.get('correct'),
                'is_correct': is_correct,
                'explanation': question.get('explanation', ''),
                'options': question.get('options', []) if question.get('type') == 'mcq' else None
            })
    
    except Exception as e:
        print(f"Error validating quiz answers: {e}")
        # Fallback scoring
        score = len(answers) // 2  # Give 50% as fallback
        detailed_results = [{'error': 'Could not validate answers properly'}]
    
    percentage_score = (score / total_questions) * 100 if total_questions > 0 else 0
    
    # Update user progress (you'll need to implement this based on your progress tracking)
    try:
        from progress import complete_quiz
        # This would be called separately by the frontend
        pass
    except ImportError:
        pass
    
    response = {
        'success': True,
        'quiz_id': quiz_id,
        'score': score,
        'total_questions': total_questions,
        'percentage': round(percentage_score, 1),
        'passed': percentage_score >= 70,  # 70% passing grade
        'detailed_results': detailed_results,
        'performance_level': _get_performance_level(percentage_score),
        'recommendations': _get_recommendations(percentage_score, topic)
    }
    
    return jsonify(response), 200

@quiz_bp.route('/quiz/custom', methods=['POST'])
@token_required
def generate_custom_quiz(current_user):
    data = request.get_json()
    language = data.get('language')
    topics = data.get('topics', [])
    difficulty = data.get('difficulty', 'Medium')
    num_questions = data.get('num_questions', 10)
    
    if not language or not topics:
        return jsonify({'error': 'Language and topics are required'}), 400
    
    try:
        questions = get_ai_service().generate_custom_quiz(language, topics, num_questions)
        
        quiz_response = {
            'success': True,
            'quiz_id': f"custom_{language}_{random.randint(1000, 9999)}",
            'language': language,
            'topics': topics,
            'difficulty': difficulty,
            'questions': questions,
            'total_questions': len(questions),
            'time_limit': _calculate_time_limit(difficulty, len(questions)),
            'source': 'ai_custom'
        }
        
        return jsonify(quiz_response), 200
        
    except Exception as e:
        print(f"Custom quiz generation failed: {e}")
        return jsonify({'error': 'Failed to generate custom quiz'}), 500

def _calculate_time_limit(difficulty: str, num_questions: int) -> int:
    """Calculate time limit based on difficulty and number of questions"""
    base_time_per_question = {
        'Easy': 2,     # 2 minutes per question
        'Medium': 3,   # 3 minutes per question
        'Hard': 5,     # 5 minutes per question
        'Expert': 8    # 8 minutes per question
    }
    
    return base_time_per_question.get(difficulty, 3) * num_questions

def _get_quiz_instructions(difficulty: str) -> str:
    """Get instructions based on difficulty level"""
    instructions = {
        'Easy': 'Answer basic questions about the topic. Each question has one correct answer.',
        'Medium': 'Mix of multiple choice and simple coding problems. Take your time to think through each question.',
        'Hard': 'Advanced questions requiring deeper understanding. Some may involve code analysis.',
        'Expert': 'Complex problems that test mastery of the topic. Read questions carefully.'
    }
    
    return instructions.get(difficulty, 'Answer all questions to the best of your ability.')

def _get_fallback_quiz_questions(language: str, topic: str, difficulty: str, num_questions: int) -> list:
    """Get fallback questions when AI service fails"""
    # Basic fallback questions for common topics
    fallback_questions = {
        'Python': {
            'Variables and Data Types': [
                {
                    'type': 'mcq',
                    'question': 'Which of the following is a valid variable name in Python?',
                    'options': ['2variable', '_variable', 'variable-name', 'variable name'],
                    'correct': 1,
                    'explanation': 'Variable names can start with letters or underscores, followed by letters, digits, or underscores.'
                },
                {
                    'type': 'mcq',
                    'question': 'What is the data type of the value 3.14 in Python?',
                    'options': ['int', 'float', 'str', 'bool'],
                    'correct': 1,
                    'explanation': 'Decimal numbers are automatically assigned the float data type in Python.'
                }
            ]
        }
    }
    
    # Try to get specific questions
    if (language in fallback_questions and 
        topic in fallback_questions[language]):
        available_questions = fallback_questions[language][topic]
        return available_questions[:num_questions]
    
    # Return generic questions if specific ones aren't available
    return [
        {
            'type': 'mcq',
            'question': f'What is the primary focus when learning {topic} in {language}?',
            'options': [
                'Understanding syntax and basic concepts',
                'Memorizing all possible functions',
                'Writing complex algorithms immediately',
                'Ignoring best practices'
            ],
            'correct': 0,
            'explanation': f'When learning {topic} in {language}, it\'s important to first understand the fundamental syntax and concepts before moving to more complex implementations.'
        }
    ]

def _get_performance_level(percentage: float) -> str:
    """Get performance level description based on percentage score"""
    if percentage >= 90:
        return 'Excellent'
    elif percentage >= 80:
        return 'Good'
    elif percentage >= 70:
        return 'Satisfactory'
    elif percentage >= 60:
        return 'Needs Improvement'
    else:
        return 'Requires More Study'

def _get_recommendations(percentage: float, topic: str) -> list:
    """Get study recommendations based on performance"""
    if percentage >= 80:
        return [
            f'Great job on {topic}! You have a solid understanding.',
            'Consider moving to the next topic or trying a harder difficulty.',
            'Practice implementing what you\'ve learned in real projects.'
        ]
    elif percentage >= 60:
        return [
            f'You have a basic understanding of {topic}, but there\'s room for improvement.',
            'Review the tutorial content again, focusing on areas you missed.',
            'Try practicing with additional examples and exercises.'
        ]
    else:
        return [
            f'You may need to spend more time studying {topic}.',
            'Go through the tutorial content step by step.',
            'Take notes and practice with simple examples.',
            'Don\'t hesitate to retake the quiz after studying.'
        ]
