const API_BASE_URL = 'http://localhost:5000/api';

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  getAuthHeaders() {
    const token = localStorage.getItem('token');
    return {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` })
    };
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: this.getAuthHeaders(),
      ...options
    };

    try {
      const response = await fetch(url, config);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || 'An error occurred');
      }

      return data;
    } catch (error) {
      throw error;
    }
  }

  // Auth methods
  async register(username, password) {
    return this.request('/register', {
      method: 'POST',
      body: JSON.stringify({ username, password })
    });
  }

  async login(username, password) {
    return this.request('/login', {
      method: 'POST',
      body: JSON.stringify({ username, password })
    });
  }

  // Progress methods
  async getUserProgress() {
    return this.request('/user/progress');
  }

  async updateProgress(language, topic, quizScore = null) {
    return this.request('/user/progress', {
      method: 'POST',
      body: JSON.stringify({ language, topic, quiz_score: quizScore })
    });
  }

  // Tutor methods
  async getTutorContent(language, topic) {
    return this.request(`/tutor/content?language=${language}&topic=${encodeURIComponent(topic)}`);
  }

  async getAvailableTopics(language) {
    return this.request(`/tutor/topics?language=${language}`);
  }

  async getTopicNotes(language, topic) {
    return this.request(`/tutor/notes?language=${language}&topic=${encodeURIComponent(topic)}`);
  }

  // Quiz methods
  async generateQuiz(language, topic, difficulty = 'Easy', numQuestions = 5) {
    return this.request('/quiz/generate', {
      method: 'POST',
      body: JSON.stringify({ 
        language, 
        topic, 
        difficulty,
        num_questions: numQuestions
      })
    });
  }

  async submitQuiz(quizId, answers, language, topic, difficulty) {
    return this.request('/quiz/submit', {
      method: 'POST',
      body: JSON.stringify({ 
        quiz_id: quizId, 
        answers, 
        language, 
        topic, 
        difficulty 
      })
    });
  }

  async generateCustomQuiz(language, topics) {
    return this.request('/quiz/custom', {
      method: 'POST',
      body: JSON.stringify({ language, topics })
    });
  }

  // Progress tracking methods
  async getTopicsWithProgress(language) {
    return this.request(`/topics/${language}`);
  }

  async completeTutorial(language, topic) {
    return this.request('/complete-tutorial', {
      method: 'POST',
      body: JSON.stringify({ language, topic })
    });
  }

  async completeQuiz(language, topic, score) {
    return this.request('/complete-quiz', {
      method: 'POST',
      body: JSON.stringify({ language, topic, score })
    });
  }

  // Compiler methods
  async runCode(code, language) {
    return this.request('/run_code', {
      method: 'POST',
      body: JSON.stringify({ code, language })
    });
  }
}

export default new ApiService();
