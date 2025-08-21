import os
import google.generativeai as genai
import json
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
            self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def _clean_json_response(self, response_text: str) -> str:
        """Clean JSON response by removing markdown code blocks"""
        # Remove markdown code blocks if present
        if response_text.strip().startswith('```'):
            # Find the first occurrence of ``` and remove it
            start_idx = response_text.find('```')
            if start_idx != -1:
                # Find the end of the opening ```json or ```
                end_start = response_text.find('\n', start_idx)
                if end_start != -1:
                    # Find the closing ```
                    end_idx = response_text.rfind('```')
                    if end_idx != -1 and end_idx != start_idx:
                        return response_text[end_start + 1:end_idx].strip()
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
        """Generate quiz questions for a topic"""
        
        difficulty_descriptions = {
            'Easy': 'Basic concepts, simple multiple choice',
            'Medium': 'Intermediate concepts, mix of MCQ and simple coding',
            'Hard': 'Advanced concepts, complex MCQ and coding problems',
            'Nightmare': 'Expert level, complex coding and debugging challenges'
        }
        
        prompt = f"""
        Generate {num_questions} quiz questions for {topic} in {language} programming.
        
        Difficulty: {difficulty} - {difficulty_descriptions.get(difficulty, '')}
        
        Question types:
        - Easy: Only MCQ questions
        - Medium: 70% MCQ, 30% coding
        - Hard: 50% MCQ, 50% coding/debugging
        - Nightmare: 30% MCQ, 70% coding/debugging
        
        Format each question as JSON:
        {{
            "type": "mcq|coding|debugging",
            "question": "Question text",
            "options": ["A", "B", "C", "D"] (for MCQ only),
            "correct": 0 (index for MCQ) or "solution description" (for coding),
            "explanation": "Why this is correct..."
        }}
        
        Return as JSON array of questions.
        """
        
        try:
            if not self.model:
                raise Exception("Google Gemini API not configured")
                
            response = self.model.generate_content(prompt)
            content = self._clean_json_response(response.text)
            return json.loads(content)
            
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
