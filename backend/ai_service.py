import os
import google.generativeai as genai
import json
import re
from typing import List, Dict, Any

class AIService:
    def __init__(self):
        # Initialize Google Gemini client
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            print("Warning: GOOGLE_API_KEY not found. AI features will use fallback content.")
            self.model = None
        else:
            genai.configure(api_key=api_key)
            # Use the latest model with generation config for better control
            generation_config = {
                "temperature": 0.7,
                "top_p": 0.8,
                "top_k": 40,
                "max_output_tokens": 2048,
            }
            self.model = genai.GenerativeModel(
                model_name='gemini-1.5-flash',
                generation_config=generation_config
            )
    
    def _clean_json_response(self, response_text: str) -> str:
        """Clean JSON response by removing markdown code blocks and formatting issues"""
        try:
            # Remove markdown code blocks if present
            text = response_text.strip()
            
            # Handle markdown code blocks
            if text.startswith('```'):
                # Find the first newline after ```
                start_idx = text.find('\n')
                if start_idx != -1:
                    # Find the closing ```
                    end_idx = text.rfind('```')
                    if end_idx != -1 and end_idx != 0:
                        text = text[start_idx + 1:end_idx].strip()
            
            # Remove any extra whitespace and ensure it's valid JSON
            text = re.sub(r'\s+', ' ', text)
            text = text.replace('\n', '').replace('\r', '')
            
            # Try to parse to validate JSON
            json.loads(text)
            return text
            
        except (json.JSONDecodeError, Exception) as e:
            print(f"JSON cleaning failed: {e}")
            return response_text.strip()
        
    def generate_tutorial_content(self, language: str, topic: str) -> Dict[str, Any]:
        """Generate tutorial content for a specific programming topic"""
        
        prompt = f"""
        Create an interactive tutorial for learning {topic} in {language} programming.
        
        Requirements:
        1. Break down the content into 6-8 digestible segments
        2. Each segment should be 1-2 sentences explaining a key concept
        3. Create 3-4 checkpoint questions to verify understanding
        4. Make it beginner-friendly but comprehensive
        5. Include practical examples where relevant
        
        Format the response as JSON with this structure:
        {{
            "content": [
                "First concept explanation...",
                "Second concept explanation...",
                ...
            ],
            "checkpoints": [
                "Do you understand what variables are?",
                "Are you clear about data types?",
                ...
            ]
        }}
        
        Topic: {topic}
        Language: {language}
        """
        
        try:
            if not self.model:
                raise Exception("Google Gemini API not configured")
                
            response = self.model.generate_content(prompt)
            content = self._clean_json_response(response.text)
            return json.loads(content)
            
        except Exception as e:
            print(f"AI API Error: {e}")
            # Fallback to hardcoded content if API fails
            return self._get_fallback_content(language, topic)
    
    def generate_comprehensive_notes(self, language: str, topic: str) -> str:
        """Generate comprehensive notes for a topic"""
        
        prompt = f"""
        Create comprehensive study notes for {topic} in {language} programming.
        
        Requirements:
        1. Use Markdown formatting
        2. Include clear headings and subheadings
        3. Provide code examples with explanations
        4. Cover syntax, use cases, and best practices
        5. Add practical examples and common pitfalls
        6. Make it suitable for both learning and reference
        
        Topic: {topic}
        Language: {language}
        
        Format as a complete Markdown document.
        """
        
        try:
            if not self.model:
                raise Exception("Google Gemini API not configured")
                
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            print(f"AI API Error: {e}")
            return self._get_fallback_notes(language, topic)
    
    def generate_quiz_questions(self, language: str, topic: str, difficulty: str, num_questions: int = 5) -> List[Dict]:
        """Generate quiz questions for a topic with improved error handling"""
        
        difficulty_descriptions = {
            'Easy': 'Basic concepts, simple multiple choice questions',
            'Medium': 'Intermediate concepts, mix of MCQ and simple coding problems',
            'Hard': 'Advanced concepts, complex MCQ and coding challenges',
            'Expert': 'Expert level, complex coding and debugging problems'
        }
        
        prompt = f"""
        Generate exactly {num_questions} quiz questions for "{topic}" in {language} programming.
        
        Difficulty Level: {difficulty} - {difficulty_descriptions.get(difficulty, 'Mixed difficulty')}
        
        Requirements:
        1. Each question must test understanding of {topic}
        2. Provide clear, unambiguous questions
        3. Include detailed explanations for each answer
        4. For MCQ questions, provide 4 options with exactly one correct answer
        5. Make sure code examples are syntactically correct
        
        Return ONLY a JSON array in this exact format:
        [
            {{
                "type": "mcq",
                "question": "Clear question text about {topic}",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct": 0,
                "explanation": "Detailed explanation of why this answer is correct"
            }}
        ]
        
        Generate {num_questions} questions following this format exactly.
        """
        
        try:
            if not self.model:
                print("AI model not available, using fallback questions")
                return self._get_fallback_questions(language, topic, difficulty)
            
            print(f"Generating {num_questions} quiz questions for {language} - {topic} ({difficulty})")
            response = self.model.generate_content(prompt)
            
            if not response or not response.text:
                print("Empty response from AI, using fallback")
                return self._get_fallback_questions(language, topic, difficulty)
            
            print("AI response received, cleaning JSON...")
            cleaned_content = self._clean_json_response(response.text)
            
            print(f"Parsing JSON: {cleaned_content[:100]}...")
            questions = json.loads(cleaned_content)
            
            # Validate the response
            if not isinstance(questions, list) or len(questions) == 0:
                print("Invalid question format, using fallback")
                return self._get_fallback_questions(language, topic, difficulty)
            
            # Validate each question structure
            valid_questions = []
            for q in questions:
                if (isinstance(q, dict) and 
                    'type' in q and 
                    'question' in q and 
                    'explanation' in q):
                    valid_questions.append(q)
            
            if len(valid_questions) == 0:
                print("No valid questions found, using fallback")
                return self._get_fallback_questions(language, topic, difficulty)
            
            print(f"Successfully generated {len(valid_questions)} questions")
            return valid_questions[:num_questions]  # Ensure we don't exceed requested number
            
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            return self._get_fallback_questions(language, topic, difficulty)
        except Exception as e:
            print(f"AI API Error: {e}")
            return self._get_fallback_questions(language, topic, difficulty)
    
    def generate_custom_quiz(self, language: str, topics: List[str], num_questions: int = 10) -> List[Dict]:
        """Generate a custom quiz from multiple topics"""
        
        prompt = f"""
        Create a comprehensive quiz mixing content from these {language} programming topics:
        {', '.join(topics)}
        
        Requirements:
        1. Generate {num_questions} questions total
        2. Distribute questions evenly across topics
        3. Mix difficulty levels (30% easy, 40% medium, 30% hard)
        4. Include various question types (MCQ, coding, debugging)
        5. Ensure questions test understanding across different topics
        
        Return as JSON array with same format as previous examples.
        """
        
        try:
            if not self.model:
                raise Exception("Google Gemini API not configured")
                
            response = self.model.generate_content(prompt)
            content = self._clean_json_response(response.text)
            return json.loads(content)
            
        except Exception as e:
            print(f"AI API Error: {e}")
            return self._get_fallback_custom_quiz(language, topics)
    
    def _get_fallback_content(self, language: str, topic: str) -> Dict[str, Any]:
        """Fallback content if AI API fails"""
        return {
            "content": [
                f"Welcome to {topic} in {language}!",
                "This is fallback content when AI API is unavailable.",
                "Please check your API configuration."
            ],
            "checkpoints": [
                "Do you understand this is fallback content?",
                "Ready to configure the AI API?"
            ]
        }
    
    def _get_fallback_notes(self, language: str, topic: str) -> str:
        return f"# {topic} in {language}\n\nAI API unavailable. Please configure your API key."
    
    def _get_fallback_questions(self, language: str, topic: str, difficulty: str) -> List[Dict]:
        return [
            {
                "type": "mcq",
                "question": f"This is a fallback question for {topic} in {language}",
                "options": ["Configure AI API", "Check API key", "Restart server", "All of above"],
                "correct": 3,
                "explanation": "AI API is not configured properly."
            }
        ]
    
    def _get_fallback_custom_quiz(self, language: str, topics: List[str]) -> List[Dict]:
        return self._get_fallback_questions(language, ", ".join(topics), "Easy")

# Global AI service instance (lazy initialization)
_ai_service_instance = None

def get_ai_service():
    """Get or create the AI service instance"""
    global _ai_service_instance
    if _ai_service_instance is None:
        _ai_service_instance = AIService()
    return _ai_service_instance

# Don't create the instance at module level to avoid environment variable issues
