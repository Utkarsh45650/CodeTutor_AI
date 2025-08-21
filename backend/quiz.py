from flask import Blueprint, request, jsonify
from auth import token_required
from ai_service import get_ai_service
import random

quiz_bp = Blueprint('quiz', __name__)

# Use AI service or fallback to hardcoded data
def get_quiz_questions():
    return {
        'C': {
            'Variables and Data Types': {
                'Easy': [
                    {
                        'type': 'mcq',
                        'question': 'Which of the following is a valid variable declaration in C?',
                        'options': ['int 123var;', 'int var123;', 'int var-123;', 'int var 123;'],
                        'correct': 1,
                        'explanation': 'Variable names must start with a letter or underscore, followed by letters, digits, or underscores.'
                    },
                    {
                        'type': 'mcq',
                        'question': 'What is the size of an int data type in most modern systems?',
                        'options': ['2 bytes', '4 bytes', '8 bytes', '1 byte'],
                        'correct': 1,
                        'explanation': 'On most modern 32-bit and 64-bit systems, int is typically 4 bytes (32 bits).'
                    },
                    {
                        'type': 'mcq',
                        'question': 'Which data type is used to store a single character in C?',
                        'options': ['string', 'char', 'character', 'text'],
                        'correct': 1,
                        'explanation': 'The char data type is used to store a single character in C.'
                    }
                ],
                'Medium': [
                    {
                        'type': 'mcq',
                        'question': 'What will be the output of: printf("%d", sizeof(float));',
                        'options': ['2', '4', '8', 'Depends on system'],
                        'correct': 1,
                        'explanation': 'float is typically 4 bytes on most systems following IEEE 754 standard.'
                    },
                    {
                        'type': 'coding',
                        'question': 'Write a C program that declares variables of different data types and prints their values.',
                        'expected_output': 'Program should declare int, float, char variables and print them',
                        'test_cases': [
                            {'input': '', 'expected': 'Should print variable values'}
                        ]
                    }
                ],
                'Hard': [
                    {
                        'type': 'mcq',
                        'question': 'Which of the following statements about variable scope in C is correct?',
                        'options': [
                            'Global variables are stored in heap memory',
                            'Local variables are automatically initialized to zero',
                            'Static local variables retain their values between function calls',
                            'Auto variables can be accessed from any function'
                        ],
                        'correct': 2,
                        'explanation': 'Static local variables maintain their values between function calls and are initialized only once.'
                    },
                    {
                        'type': 'coding',
                        'question': 'Write a C program that demonstrates the difference between local and global variables.',
                        'expected_output': 'Program should show scope differences',
                        'test_cases': []
                    }
                ],
                'Nightmare': [
                    {
                        'type': 'mcq',
                        'question': 'In C, what happens when you access an uninitialized local variable?',
                        'options': [
                            'It always contains zero',
                            'It contains garbage value',
                            'Compilation error occurs',
                            'Runtime error occurs'
                        ],
                        'correct': 1,
                        'explanation': 'Uninitialized local variables contain garbage values (whatever was previously in that memory location).'
                    },
                    {
                        'type': 'debugging',
                        'question': 'Find and fix the bug in this code:\n```c\nint main() {\n    int x;\n    printf("Value: %d", x);\n    return 0;\n}\n```',
                        'expected_fix': 'Initialize variable x before using it'
                    }
                ]
            },
            'Control Structures': {
                'Easy': [
                    {
                        'type': 'mcq',
                        'question': 'Which keyword is used for conditional execution in C?',
                        'options': ['when', 'if', 'condition', 'check'],
                        'correct': 1,
                        'explanation': 'The if keyword is used for conditional execution in C.'
                    },
                    {
                        'type': 'mcq',
                        'question': 'What is the correct syntax for a for loop in C?',
                        'options': [
                            'for (init; condition; increment)',
                            'for init; condition; increment',
                            'for (init, condition, increment)',
                            'for init, condition, increment'
                        ],
                        'correct': 0,
                        'explanation': 'The correct syntax uses semicolons to separate the three parts within parentheses.'
                    }
                ]
            }
        },
        'Python': {
            'Variables and Data Types': {
                'Easy': [
                    {
                        'type': 'mcq',
                        'question': 'Which of the following is a valid way to create a variable in Python?',
                        'options': ['int x = 5', 'x = 5', 'var x = 5', 'x := 5'],
                        'correct': 1,
                        'explanation': 'Python uses simple assignment (x = 5) without type declarations.'
                    },
                    {
                        'type': 'mcq',
                        'question': 'What type of data does the variable store: x = "Hello"',
                        'options': ['int', 'float', 'str', 'char'],
                        'correct': 2,
                        'explanation': 'Text enclosed in quotes creates a string (str) type in Python.'
                    }
                ],
                'Medium': [
                    {
                        'type': 'mcq',
                        'question': 'What will be the output of: print(type([1, 2, 3]))',
                        'options': ['<class "list">', '<class "tuple">', '<class "array">', '<class "dict">'],
                        'correct': 0,
                        'explanation': 'Square brackets create a list object in Python.'
                    },
                    {
                        'type': 'coding',
                        'question': 'Create variables of different types and print their types using the type() function.',
                        'expected_output': 'Should print types of different variables',
                        'test_cases': []
                    }
                ]
            }
        }
        # Add more questions for other languages and topics
    }

@quiz_bp.route('/quiz/generate', methods=['POST'])
@token_required
def generate_quiz(current_user):
    data = request.get_json()
    language = data.get('language')
    topic = data.get('topic')
    difficulty = data.get('difficulty', 'Easy')
    
    if not language or not topic:
        return jsonify({'error': 'Language and topic are required'}), 400
    
    # Try AI service first, fallback to hardcoded questions
    try:
        ai_questions = get_ai_service().generate_quiz_questions(language, topic, difficulty, 5)
        return jsonify({
            'quiz_id': f"{language}_{topic}_{difficulty}_{random.randint(1000, 9999)}",
            'language': language,
            'topic': topic,
            'difficulty': difficulty,
            'questions': ai_questions,
            'time_limit': 15  # minutes
        }), 200
    except Exception as e:
        print(f"AI service failed, using fallback: {e}")
        # Fallback to hardcoded content
        quiz_questions = get_quiz_questions()
        
        if language not in quiz_questions or topic not in quiz_questions[language]:
            return jsonify({'error': 'Quiz not available for this topic'}), 404
        
        if difficulty not in quiz_questions[language][topic]:
            return jsonify({'error': 'Difficulty level not available'}), 404
        
        questions = quiz_questions[language][topic][difficulty]
        
        # Randomize question order
        randomized_questions = random.sample(questions, min(len(questions), 5))
        
        return jsonify({
            'quiz_id': f"{language}_{topic}_{difficulty}_{random.randint(1000, 9999)}",
            'language': language,
            'topic': topic,
            'difficulty': difficulty,
            'questions': randomized_questions,
            'time_limit': 15  # minutes
        }), 200

@quiz_bp.route('/quiz/submit', methods=['POST'])
@token_required
def submit_quiz(current_user):
    data = request.get_json()
    quiz_id = data.get('quiz_id')
    answers = data.get('answers', [])
    language = data.get('language')
    topic = data.get('topic')
    difficulty = data.get('difficulty')
    
    if not quiz_id or not language or not topic:
        return jsonify({'error': 'Quiz ID, language, and topic are required'}), 400
    
    # Get original questions to check answers
    quiz_questions = get_quiz_questions()
    if language not in quiz_questions or topic not in quiz_questions[language] or difficulty not in quiz_questions[language][topic]:
        return jsonify({'error': 'Quiz not found'}), 404
    
    questions = quiz_questions[language][topic][difficulty]
    
    # Calculate score
    correct_answers = 0
    total_questions = len(answers)
    results = []
    
    for i, answer in enumerate(answers):
        if i < len(questions):
            question = questions[i]
            is_correct = False
            
            if question['type'] == 'mcq':
                is_correct = answer == question['correct']
            elif question['type'] == 'coding':
                # For coding questions, mark as correct if answer is provided
                # TODO: Implement proper code evaluation
                is_correct = len(str(answer).strip()) > 10
            elif question['type'] == 'debugging':
                # For debugging questions, check if fix is provided
                is_correct = len(str(answer).strip()) > 5
            
            if is_correct:
                correct_answers += 1
            
            results.append({
                'question_index': i,
                'question': question['question'],
                'user_answer': answer,
                'correct_answer': question.get('correct', 'Code solution required'),
                'is_correct': is_correct,
                'explanation': question.get('explanation', 'No explanation available')
            })
    
    score = (correct_answers / total_questions * 100) if total_questions > 0 else 0
    
    return jsonify({
        'quiz_id': quiz_id,
        'score': round(score, 2),
        'correct_answers': correct_answers,
        'total_questions': total_questions,
        'results': results,
        'passed': score >= 60  # 60% passing grade
    }), 200

@quiz_bp.route('/quiz/custom', methods=['POST'])
@token_required
def generate_custom_quiz(current_user):
    data = request.get_json()
    language = data.get('language')
    topics = data.get('topics', [])
    
    if not language or len(topics) < 2:
        return jsonify({'error': 'Language and at least 2 topics are required'}), 400
    
    # Try AI service first, fallback to hardcoded questions
    try:
        ai_questions = get_ai_service().generate_custom_quiz(language, topics, 10)
        return jsonify({
            'quiz_id': f"custom_{language}_{random.randint(1000, 9999)}",
            'language': language,
            'topics': topics,
            'difficulty': 'Mixed',
            'questions': ai_questions,
            'time_limit': 20  # minutes for custom quiz
        }), 200
    except Exception as e:
        print(f"AI service failed, using fallback: {e}")
        # Fallback to hardcoded content
        quiz_questions = get_quiz_questions()
        
        if language not in quiz_questions:
            return jsonify({'error': 'Language not supported'}), 404
        
        # Collect questions from selected topics
        all_questions = []
        for topic in topics:
            if topic in quiz_questions[language]:
                # Mix questions from different difficulty levels
                for difficulty in ['Easy', 'Medium', 'Hard']:
                    if difficulty in quiz_questions[language][topic]:
                        questions = quiz_questions[language][topic][difficulty]
                        # Take 1-2 questions from each difficulty
                        selected = random.sample(questions, min(2, len(questions)))
                        all_questions.extend(selected)
        
        # Randomize and limit to 10 questions
        final_questions = random.sample(all_questions, min(10, len(all_questions)))
        
        return jsonify({
            'quiz_id': f"custom_{language}_{random.randint(1000, 9999)}",
            'language': language,
            'topics': topics,
            'difficulty': 'Mixed',
            'questions': final_questions,
            'time_limit': 20  # minutes for custom quiz
        }), 200
