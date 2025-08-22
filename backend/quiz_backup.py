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
            
            # Format the response properly
            quiz_response = {
                'success': True,
                'quiz_id': f"{language}_{topic}_{difficulty}_{random.randint(1000, 9999)}",
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
        
        quiz_response = {
            'success': True,
            'quiz_id': f"{language}_{topic}_{difficulty}_{random.randint(1000, 9999)}",
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
    quiz_questions = get_quiz_questions()
    
    # Try to get questions for the specific language and topic
    if (language in quiz_questions and 
        topic in quiz_questions[language] and 
        difficulty in quiz_questions[language][topic]):
        
        available_questions = quiz_questions[language][topic][difficulty]
        return available_questions[:num_questions]
    
    # If no specific questions available, return generic programming questions
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
