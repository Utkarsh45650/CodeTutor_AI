import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import apiService from '../../utils/api';
import CodeEditor from '../Compiler/CodeEditor';
import styles from './QuizInterface.module.css';

const QuizInterface = () => {
  const { language, topic } = useParams();
  const navigate = useNavigate();
  const [quiz, setQuiz] = useState(null);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState([]);
  const [timeLeft, setTimeLeft] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [difficulty, setDifficulty] = useState('Easy');
  const [quizStarted, setQuizStarted] = useState(false);

  useEffect(() => {
    if (quizStarted && timeLeft > 0) {
      const timer = setTimeout(() => {
        setTimeLeft(timeLeft - 1);
      }, 1000);
      return () => clearTimeout(timer);
    } else if (timeLeft === 0 && quizStarted) {
      handleSubmitQuiz();
    }
  }, [timeLeft, quizStarted]);

  const startQuiz = async () => {
    try {
      setLoading(true);
      const response = await apiService.generateQuiz(language, topic, difficulty);
      setQuiz(response);
      setAnswers(new Array(response.questions.length).fill(''));
      setTimeLeft(response.time_limit * 60); // Convert minutes to seconds
      setQuizStarted(true);
    } catch (error) {
      setError('Failed to generate quiz');
    } finally {
      setLoading(false);
    }
  };

  const handleAnswerChange = (value) => {
    const newAnswers = [...answers];
    newAnswers[currentQuestion] = value;
    setAnswers(newAnswers);
  };

  const handleNext = () => {
    if (currentQuestion < quiz.questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
    }
  };

  const handlePrevious = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(currentQuestion - 1);
    }
  };

  const handleSubmitQuiz = async () => {
    try {
      const response = await apiService.submitQuiz(
        quiz.quiz_id,
        answers,
        language,
        topic,
        difficulty
      );
      
      // Update progress if quiz is passed
      if (response.passed) {
        await apiService.updateProgress(language, topic, response.score);
      }
      
      navigate('/quiz-results', { 
        state: { 
          results: response,
          language,
          topic,
          difficulty 
        } 
      });
    } catch (error) {
      setError('Failed to submit quiz');
    }
  };

  const formatTime = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
  };

  const getCurrentQuestion = () => {
    return quiz?.questions[currentQuestion];
  };

  if (!quizStarted) {
    return (
      <div className={styles.quizSetup}>
        <div className="page-container">
          <div className={styles.setupCard}>
            <h1>Quiz Setup</h1>
            <p>Ready to test your knowledge of <strong>{topic}</strong> in {language}?</p>
            
            <div className={styles.difficultySelection}>
              <h3>Select Difficulty Level:</h3>
              <div className={styles.difficultyOptions}>
                {['Easy', 'Medium', 'Hard', 'Nightmare'].map(level => (
                  <button
                    key={level}
                    onClick={() => setDifficulty(level)}
                    className={`btn ${difficulty === level ? 'btn-primary' : 'btn-secondary'}`}
                  >
                    {level}
                  </button>
                ))}
              </div>
              
              <div className={styles.difficultyInfo}>
                {difficulty === 'Easy' && (
                  <p>🟢 Basic multiple-choice questions on fundamental concepts</p>
                )}
                {difficulty === 'Medium' && (
                  <p>🟡 Advanced MCQs + one coding problem</p>
                )}
                {difficulty === 'Hard' && (
                  <p>🟠 Complex MCQs + multiple coding problems</p>
                )}
                {difficulty === 'Nightmare' && (
                  <p>🔴 In-depth MCQs + complex coding + debugging challenges</p>
                )}
              </div>
            </div>
            
            {error && (
              <div className="error-message">
                {error}
              </div>
            )}
            
            <div className={styles.setupActions}>
              <Link to="/dashboard" className="btn btn-secondary">
                Cancel
              </Link>
              <button 
                onClick={startQuiz}
                disabled={loading}
                className="btn btn-primary"
              >
                {loading ? 'Generating Quiz...' : 'Start Quiz'}
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className={styles.loadingContainer}>
        <div className="loading-spinner"></div>
        <p>Loading quiz...</p>
      </div>
    );
  }

  const currentQuestionData = getCurrentQuestion();
  const progress = ((currentQuestion + 1) / quiz.questions.length) * 100;

  return (
    <div className={styles.quizInterface}>
      <div className="page-container">
        <header className={styles.header}>
          <div className={styles.quizInfo}>
            <h1>{language} - {topic} Quiz</h1>
            <span className={styles.difficulty}>Difficulty: {difficulty}</span>
          </div>
          
          <div className={styles.timer}>
            <span className={timeLeft < 300 ? styles.timerWarning : ''}>
              ⏰ {formatTime(timeLeft)}
            </span>
          </div>
        </header>

        <div className={styles.progressSection}>
          <div className={styles.progressBar}>
            <div 
              className={styles.progressFill}
              style={{ width: `${progress}%` }}
            ></div>
          </div>
          <span className={styles.progressText}>
            Question {currentQuestion + 1} of {quiz.questions.length}
          </span>
        </div>

        <main className={styles.questionSection}>
          <div className={styles.questionCard}>
            <h2 className={styles.questionTitle}>
              {currentQuestionData?.type === 'mcq' && '📝'}
              {currentQuestionData?.type === 'coding' && '💻'}
              {currentQuestionData?.type === 'debugging' && '🐛'}
              Question {currentQuestion + 1}
            </h2>
            
            <p className={styles.questionText}>
              {currentQuestionData?.question}
            </p>

            {currentQuestionData?.type === 'mcq' && (
              <div className={styles.mcqOptions}>
                {currentQuestionData.options?.map((option, index) => (
                  <button
                    key={index}
                    onClick={() => handleAnswerChange(index)}
                    className={`${styles.optionButton} ${
                      answers[currentQuestion] === index ? styles.selected : ''
                    }`}
                  >
                    <span className={styles.optionLabel}>
                      {String.fromCharCode(65 + index)}
                    </span>
                    {option}
                  </button>
                ))}
              </div>
            )}

            {(currentQuestionData?.type === 'coding' || currentQuestionData?.type === 'debugging') && (
              <div className={styles.codingSection}>
                <CodeEditor
                  language={language}
                  onResult={(result) => {
                    // Store the code as the answer
                    handleAnswerChange(result.success ? 'correct' : 'incorrect');
                  }}
                />
                <textarea
                  value={answers[currentQuestion] || ''}
                  onChange={(e) => handleAnswerChange(e.target.value)}
                  placeholder="Enter your code solution here..."
                  className={styles.codeAnswer}
                  rows={10}
                />
              </div>
            )}
          </div>
        </main>

        <footer className={styles.navigation}>
          <button
            onClick={handlePrevious}
            disabled={currentQuestion === 0}
            className="btn btn-secondary"
          >
            ← Previous
          </button>
          
          <div className={styles.questionIndicators}>
            {quiz.questions.map((_, index) => (
              <button
                key={index}
                onClick={() => setCurrentQuestion(index)}
                className={`${styles.indicator} ${
                  index === currentQuestion ? styles.current : ''
                } ${
                  answers[index] !== '' ? styles.answered : ''
                }`}
              >
                {index + 1}
              </button>
            ))}
          </div>
          
          {currentQuestion === quiz.questions.length - 1 ? (
            <button
              onClick={handleSubmitQuiz}
              className="btn btn-success"
            >
              Submit Quiz
            </button>
          ) : (
            <button
              onClick={handleNext}
              className="btn btn-primary"
            >
              Next →
            </button>
          )}
        </footer>
      </div>
    </div>
  );
};

export default QuizInterface;
