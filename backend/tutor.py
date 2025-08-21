from flask import Blueprint, request, jsonify
from auth import token_required
from ai_service import get_ai_service

tutor_bp = Blueprint('tutor', __name__)

# Use AI service or fallback to hardcoded data
def get_tutor_content_data():
    return {
        'C': {
            'Variables and Data Types': {
                'content': [
                    "Welcome to C programming! Let's start with variables and data types.",
                    "A variable is a storage location with an associated name that contains data. In C, you must declare variables before using them.",
                    "The basic syntax for declaring a variable is: data_type variable_name;",
                    "C has several built-in data types: int (integers), float (decimal numbers), char (single characters), and double (double-precision floating-point).",
                    "For example: int age = 25; declares an integer variable named 'age' and initializes it with the value 25.",
                    "Character variables use single quotes: char grade = 'A';",
                    "Float variables can store decimal values: float price = 19.99;",
                    "Remember that C is case-sensitive, so 'Age' and 'age' are different variables."
                ],
                'checkpoints': [
                    "Do you understand what a variable is and why we need to declare them in C?",
                    "Are you clear about the different data types available in C?",
                    "Do you understand the syntax for declaring and initializing variables?",
                    "Shall we move on to the next topic?"
                ]
            },
            'Control Structures': {
                'content': [
                    "Control structures allow you to control the flow of program execution.",
                    "The if statement is used for conditional execution: if (condition) { /* code */ }",
                    "You can add else clauses: if (condition) { /* code */ } else { /* other code */ }",
                    "For loops repeat code a specific number of times: for (int i = 0; i < 10; i++) { /* code */ }",
                    "While loops continue as long as a condition is true: while (condition) { /* code */ }",
                    "Switch statements provide an alternative to multiple if-else statements.",
                    "Break and continue statements help control loop execution."
                ],
                'checkpoints': [
                    "Do you understand how if statements work for making decisions?",
                    "Are you comfortable with the syntax of for and while loops?",
                    "Do you see how control structures help organize program logic?",
                    "Ready to continue to the next topic?"
                ]
            }
        },
        'Python': {
            'Variables and Data Types': {
                'content': [
                    "Python is a dynamically typed language, which means you don't need to declare variable types explicitly.",
                    "You can create a variable simply by assigning a value: name = 'Alice'",
                    "Python has several built-in data types: int, float, str (string), bool (boolean), list, dict (dictionary), and tuple.",
                    "Numbers can be integers (whole numbers) or floats (decimal numbers): age = 25, price = 19.99",
                    "Strings are sequences of characters enclosed in quotes: message = 'Hello, World!'",
                    "Booleans represent True or False values: is_active = True",
                    "Lists store multiple items: fruits = ['apple', 'banana', 'orange']",
                    "Python automatically determines the type based on the value you assign."
                ],
                'checkpoints': [
                    "Do you understand that Python doesn't require explicit type declarations?",
                    "Are you clear about the different data types in Python?",
                    "Do you see how Python makes variable creation simpler than languages like C?",
                    "Shall we proceed to the next concept?"
                ]
            },
            'Control Structures': {
                'content': [
                    "Python uses indentation to define code blocks, making it very readable.",
                    "If statements use the syntax: if condition: followed by indented code",
                    "You can add elif (else if) and else clauses for multiple conditions",
                    "For loops iterate over sequences: for item in list: or for i in range(10):",
                    "While loops continue until a condition becomes false: while condition:",
                    "Python's range() function is commonly used with for loops: range(start, stop, step)",
                    "List comprehensions provide a concise way to create lists: [x*2 for x in range(10)]"
                ],
                'checkpoints': [
                    "Do you understand how Python uses indentation instead of braces?",
                    "Are you comfortable with if, elif, and else statements?",
                    "Do you see how for loops work with different types of sequences?",
                    "Ready to move on to the next topic?"
                ]
            }
        },
        'Java': {
            'Variables and Data Types': {
                'content': [
                    "Java is a strongly typed language where every variable must be declared with a type.",
                    "The syntax for declaring variables is: dataType variableName = value;",
                    "Java has primitive data types: int, double, float, char, boolean, byte, short, long",
                    "Examples: int count = 10; double price = 15.99; boolean isValid = true;",
                    "String is a reference type (class) in Java: String name = \"John\";",
                    "Java follows camelCase naming convention for variables: firstName, lastName",
                    "Constants are declared with 'final' keyword: final double PI = 3.14159;",
                    "Java is case-sensitive, so 'Count' and 'count' are different variables."
                ],
                'checkpoints': [
                    "Do you understand Java's strong typing system?",
                    "Are you clear about primitive vs reference types?",
                    "Do you understand the naming conventions in Java?",
                    "Shall we continue to the next topic?"
                ]
            },
            'Control Structures': {
                'content': [
                    "Java control structures are similar to C/C++ with some enhancements.",
                    "If statements: if (condition) { /* code */ } else { /* code */ }",
                    "For loops: for (int i = 0; i < 10; i++) { /* code */ }",
                    "Enhanced for loop (for-each): for (Type item : collection) { /* code */ }",
                    "While and do-while loops: while (condition) { } and do { } while (condition);",
                    "Switch statements support strings (Java 7+) and expressions (Java 14+)",
                    "Break and continue work within loops and switch statements."
                ],
                'checkpoints': [
                    "Do you understand the basic if-else syntax in Java?",
                    "Are you comfortable with both traditional and enhanced for loops?",
                    "Do you see the similarities with other programming languages?",
                    "Ready to proceed to the next topic?"
                ]
            }
        },
        'C++': {
            'Variables and Data Types': {
                'content': [
                    "C++ builds upon C with additional features and type safety.",
                    "Basic data types include int, double, float, char, bool, and their variations",
                    "C++ introduces the 'auto' keyword for automatic type deduction: auto x = 10;",
                    "String handling is improved with the std::string class: std::string name = \"Alice\";",
                    "References provide an alternative to pointers: int& ref = variable;",
                    "Const keyword ensures variables cannot be modified: const int MAX_SIZE = 100;",
                    "C++ supports both C-style and modern initialization: int x{10}; (uniform initialization)"
                ],
                'checkpoints': [
                    "Do you understand how C++ extends C's type system?",
                    "Are you clear about the 'auto' keyword and when to use it?",
                    "Do you see the advantages of std::string over C-style strings?",
                    "Shall we move on to the next concept?"
                ]
            },
            'Control Structures': {
                'content': [
                    "C++ control structures are based on C with additional features.",
                    "Range-based for loops (C++11): for (auto& item : container) { }",
                    "Traditional for loops: for (int i = 0; i < size; ++i) { }",
                    "If statements with initialization (C++17): if (auto x = getValue(); x > 0) { }",
                    "Switch statements with fallthrough warnings and [[fallthrough]] attribute",
                    "While and do-while loops work the same as in C",
                    "Break and continue statements for loop control"
                ],
                'checkpoints': [
                    "Do you understand range-based for loops and their benefits?",
                    "Are you comfortable with the modern C++ features in control structures?",
                    "Do you see how C++ maintains C compatibility while adding improvements?",
                    "Ready to continue to the next topic?"
                ]
            }
        },
        'C#': {
            'Variables and Data Types': {
                'content': [
                    "C# is a strongly typed language with excellent type safety and modern features.",
                    "Basic value types: int, double, float, char, bool, decimal",
                    "Reference types: string, object, arrays, and custom classes",
                    "Var keyword for implicit typing: var name = \"Alice\"; (compiler infers string)",
                    "Nullable types: int? nullableInt = null; (can hold null values)",
                    "String interpolation: $\"Hello, {name}!\" (modern string formatting)",
                    "Properties provide controlled access to class fields with get/set accessors"
                ],
                'checkpoints': [
                    "Do you understand the difference between value and reference types?",
                    "Are you clear about when to use 'var' vs explicit types?",
                    "Do you see how string interpolation improves code readability?",
                    "Shall we proceed to the next topic?"
                ]
            },
            'Control Structures': {
                'content': [
                    "C# provides modern control structures with enhanced readability and safety.",
                    "If statements: if (condition) { } else if (condition) { } else { }",
                    "Switch expressions (C# 8.0): var result = input switch { 1 => \"One\", 2 => \"Two\" };",
                    "For loops: for (int i = 0; i < collection.Count; i++) { }",
                    "Foreach loops: foreach (var item in collection) { }",
                    "While and do-while loops for indefinite iteration",
                    "Pattern matching in switch statements for complex conditions"
                ],
                'checkpoints': [
                    "Do you understand the modern switch expression syntax?",
                    "Are you comfortable with foreach loops and their advantages?",
                    "Do you see how C# emphasizes readability and safety?",
                    "Ready to move on to the next topic?"
                ]
            }
        }
    }

@tutor_bp.route('/tutor/content', methods=['GET'])
@token_required
def get_tutor_content(current_user):
    language = request.args.get('language')
    topic = request.args.get('topic')
    
    if not language or not topic:
        return jsonify({'error': 'Language and topic are required'}), 400
    
    # Try AI service first, fallback to hardcoded data
    try:
        ai_content = get_ai_service().generate_tutorial_content(language, topic)
        return jsonify({
            'language': language,
            'topic': topic,
            'content': ai_content['content'],
            'checkpoints': ai_content['checkpoints']
        }), 200
    except Exception as e:
        print(f"AI service failed, using fallback: {e}")
        # Fallback to hardcoded content
        content_data = get_tutor_content_data()
        
        if language not in content_data or topic not in content_data[language]:
            return jsonify({'error': 'Content not found'}), 404
        
        return jsonify({
            'language': language,
            'topic': topic,
            'content': content_data[language][topic]['content'],
            'checkpoints': content_data[language][topic]['checkpoints']
        }), 200

@tutor_bp.route('/tutor/topics', methods=['GET'])
@token_required
def get_available_topics(current_user):
    language = request.args.get('language')
    
    if not language:
        return jsonify({'error': 'Language is required'}), 400
    
    # TODO: Replace with dynamic topic generation
    topics = {
        'C': ['Variables and Data Types', 'Control Structures', 'Functions', 'Arrays and Pointers'],
        'C++': ['Variables and Data Types', 'Control Structures', 'Classes and Objects', 'STL Containers'],
        'C#': ['Variables and Data Types', 'Control Structures', 'Classes and Objects', 'LINQ and Collections'],
        'Java': ['Variables and Data Types', 'Control Structures', 'Classes and Objects', 'Collections Framework'],
        'Python': ['Variables and Data Types', 'Control Structures', 'Functions and Modules', 'Data Structures']
    }
    
    return jsonify({
        'language': language,
        'topics': topics.get(language, [])
    }), 200

@tutor_bp.route('/tutor/notes', methods=['GET'])
@token_required
def get_topic_notes(current_user):
    language = request.args.get('language')
    topic = request.args.get('topic')
    
    if not language or not topic:
        return jsonify({'error': 'Language and topic are required'}), 400
    
    # Try AI service first, fallback to hardcoded notes
    try:
        ai_notes = get_ai_service().generate_comprehensive_notes(language, topic)
        return jsonify({
            'language': language,
            'topic': topic,
            'notes': ai_notes
        }), 200
    except Exception as e:
        print(f"AI service failed, using fallback: {e}")
        # Fallback to hardcoded notes
        notes = {
        'C': {
            'Variables and Data Types': """
# Variables and Data Types in C

## Overview
Variables are fundamental building blocks in C programming. They provide named storage locations for data that can be modified during program execution.

## Variable Declaration
```c
data_type variable_name;
data_type variable_name = initial_value;
```

## Basic Data Types

### Integer Types
- **int**: Standard integer (typically 32 bits)
- **short**: Short integer (typically 16 bits)
- **long**: Long integer (typically 64 bits)
- **char**: Single character (8 bits)

### Floating-Point Types
- **float**: Single-precision floating-point (32 bits)
- **double**: Double-precision floating-point (64 bits)

### Examples
```c
int age = 25;
float price = 19.99f;
char grade = 'A';
double pi = 3.14159265359;
```

## Variable Naming Rules
1. Must start with a letter or underscore
2. Can contain letters, digits, and underscores
3. Case-sensitive
4. Cannot use C keywords

## Best Practices
- Use descriptive names
- Follow consistent naming conventions
- Initialize variables before use
- Use appropriate data types for your data
            """
        },
        'Python': {
            'Variables and Data Types': """
# Variables and Data Types in Python

## Overview
Python is dynamically typed, meaning you don't need to explicitly declare variable types. The interpreter automatically determines the type based on the assigned value.

## Variable Assignment
```python
variable_name = value
```

## Basic Data Types

### Numeric Types
- **int**: Integers (unlimited precision)
- **float**: Floating-point numbers
- **complex**: Complex numbers

### Text Type
- **str**: Strings (sequences of characters)

### Boolean Type
- **bool**: True or False

### Sequence Types
- **list**: Ordered, mutable collections
- **tuple**: Ordered, immutable collections
- **range**: Sequence of numbers

### Examples
```python
age = 25                    # int
price = 19.99              # float
name = "Alice"             # str
is_student = True          # bool
fruits = ["apple", "banana"] # list
coordinates = (10, 20)     # tuple
```

## Type Checking
```python
type(variable)     # Returns the type
isinstance(variable, type)  # Checks if variable is of specific type
```

## Best Practices
- Use descriptive variable names
- Follow PEP 8 naming conventions (snake_case)
- Use type hints for better code documentation
            """
        }
        # Add more comprehensive notes for other languages and topics
    }
    
    note_content = notes.get(language, {}).get(topic, f"# {topic} in {language}\n\nNotes for this topic are being prepared...")
    
    return jsonify({
        'language': language,
        'topic': topic,
        'notes': note_content
    }), 200
