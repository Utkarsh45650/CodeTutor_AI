import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import apiService from '../../utils/api';
import styles from './QuizInterface_enhanced.module.css';

const QuizInterface = () => {
  const { language, topic } = useParams();
  
  // Quiz state
  const [quiz, setQuiz] = useState(null);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState([]);
  const [timeLeft, setTimeLeft] = useState(0);
  const [quizResults, setQuizResults] = useState(null);
  
  // UI state
  const [phase, setPhase] = useState('setup'); // setup, generating, active, completed, results
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  // Quiz configuration
  const [difficulty, setDifficulty] = useState('Easy');
  const [numQuestions, setNumQuestions] = useState(5);

  // Timer effect
  useEffect(() => {
    if (phase === 'active' && timeLeft > 0) {
      const timer = setTimeout(() => {
        setTimeLeft(timeLeft - 1);
      }, 1000);
      return () => clearTimeout(timer);
    } else if (timeLeft === 0 && phase === 'active') {
      handleSubmitQuiz();
    }
  }, [timeLeft, phase]); // eslint-disable-line react-hooks/exhaustive-deps

  const generateQuiz = async () => {
    try {
      setPhase('generating');
      setLoading(true);
      setError('');
      
      const response = await apiService.generateQuiz(language, topic, difficulty, numQuestions);
      
      if (response.success) {
        setQuiz(response);
        // Initialize answers array with null values instead of empty strings for better checking
        setAnswers(new Array(response.questions.length).fill(null));
        setTimeLeft(response.time_limit * 60); // Convert minutes to seconds
        setPhase('active');
        console.log('Quiz loaded:', response);
        console.log('Questions:', response.questions);
      } else {
        throw new Error('Failed to generate quiz');
      }
    } catch (error) {
      setError(error.message || 'Failed to generate quiz. Please try again.');
      setPhase('setup');
    } finally {
      setLoading(false);
    }
  };

  const handleAnswerChange = (value) => {
    const newAnswers = [...answers];
    newAnswers[currentQuestion] = value;
    setAnswers(newAnswers);
    console.log(`Question ${currentQuestion + 1}: Selected answer index ${value}`);
  };

  const nextQuestion = () => {
    if (currentQuestion < quiz.questions.length - 1) {
      console.log(`Moving from question ${currentQuestion + 1} to ${currentQuestion + 2}`);
      setCurrentQuestion(currentQuestion + 1);
    }
  };

  const previousQuestion = () => {
    if (currentQuestion > 0) {
      console.log(`Moving from question ${currentQuestion + 1} to ${currentQuestion}`);
      setCurrentQuestion(currentQuestion - 1);
    }
  };

  const handleSubmitQuiz = async () => {
    try {
      setPhase('completed');
      setLoading(true);
      
      console.log('Submitting quiz with answers:', answers);
      
      const response = await apiService.submitQuiz(
        quiz.quiz_id,
        answers,
        language,
        topic,
        difficulty
      );
      
      console.log('Quiz submission response:', response);
      setQuizResults(response);
      setPhase('results');
    } catch (error) {
      console.error('Quiz submission error:', error);
      setError('Failed to submit quiz. Please try again.');
      setPhase('active');
    } finally {
      setLoading(false);
    }
  };

  const formatTime = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
  };

  const getDifficultyColor = (diff) => {
    const colors = {
      'Easy': '#4CAF50',
      'Medium': '#FF9800',
      'Hard': '#F44336',
      'Expert': '#9C27B0'
    };
    return colors[diff] || '#666';
  };

  const restartQuiz = () => {
    setQuiz(null);
    setCurrentQuestion(0);
    setAnswers([]);
    setTimeLeft(0);
    setQuizResults(null);
    setPhase('setup');
    setError('');
    setLoading(false);
    console.log('Quiz restarted');
  };

  // Setup Phase
  if (phase === 'setup') {
    return (
      <div className={styles.container}>
        <div className={styles.header}>
          <Link to={`/dashboard`} className={styles.backLink}>
            ← Back to Dashboard
          </Link>
          <h1 className={styles.title}>Quiz Setup</h1>
        </div>

        <div className={styles.setupCard}>
          <div className={styles.topicInfo}>
            <h2>{language} - {topic}</h2>
            <p>Configure your quiz settings below:</p>
          </div>

          <div className={styles.configSection}>
            <div className={styles.configGroup}>
              <label className={styles.configLabel}>Difficulty Level:</label>
              <div className={styles.difficultyOptions}>
                {['Easy', 'Medium', 'Hard', 'Expert'].map((level) => (
                  <button
                    key={level}
                    className={`${styles.difficultyBtn} ${difficulty === level ? styles.active : ''}`}
                    onClick={() => setDifficulty(level)}
                    style={{
                      borderColor: difficulty === level ? getDifficultyColor(level) : '#ddd',
                      backgroundColor: difficulty === level ? getDifficultyColor(level) : 'transparent',
                      color: difficulty === level ? 'white' : getDifficultyColor(level)
                    }}
                  >
                    {level}
                  </button>
                ))}
              </div>
              <p className={styles.difficultyDescription}>
                {difficulty === 'Easy' && 'Basic concepts with simple multiple choice questions'}
                {difficulty === 'Medium' && 'Intermediate concepts with mixed question types'}
                {difficulty === 'Hard' && 'Advanced concepts requiring deeper understanding'}
                {difficulty === 'Expert' && 'Complex problems testing mastery of the topic'}
              </p>
            </div>

            <div className={styles.configGroup}>
              <label className={styles.configLabel}>Number of Questions:</label>
              <select
                className={styles.questionSelect}
                value={numQuestions}
                onChange={(e) => setNumQuestions(parseInt(e.target.value))}
              >
                <option value={3}>3 Questions (Quick)</option>
                <option value={5}>5 Questions (Standard)</option>
                <option value={8}>8 Questions (Comprehensive)</option>
                <option value={10}>10 Questions (Extended)</option>
              </select>
              <p className={styles.timeEstimate}>
                Estimated time: {((numQuestions * (difficulty === 'Easy' ? 2 : difficulty === 'Medium' ? 3 : difficulty === 'Hard' ? 5 : 8)) / 60 * 100) / 100} minutes
              </p>
            </div>
          </div>

          <button
            className={styles.generateBtn}
            onClick={generateQuiz}
            disabled={loading}
          >
            {loading ? 'Generating Quiz...' : 'Generate Quiz'}
          </button>

          {error && (
            <div className={styles.error}>
              {error}
            </div>
          )}
        </div>
      </div>
    );
  }

  // Generating Phase
  if (phase === 'generating') {
    return (
      <div className={styles.container}>
        <div className={styles.loadingCard}>
          <div className={styles.spinner}></div>
          <h2>Generating Your Quiz...</h2>
          <p>Creating {numQuestions} {difficulty.toLowerCase()} questions about {topic}</p>
          <div className={styles.loadingProgress}>
            <div className={styles.progressBar}>
              <div className={styles.progressFill}></div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Active Quiz Phase
  if (phase === 'active' && quiz) {
    const question = quiz.questions[currentQuestion];
    const progress = ((currentQuestion + 1) / quiz.questions.length) * 100;
    
    console.log(`Displaying question ${currentQuestion + 1}:`, question);
    console.log(`Current answers:`, answers);

    return (
      <div className={styles.container}>
        <div className={styles.quizHeader}>
          <div className={styles.quizInfo}>
            <h2>{quiz.language} - {quiz.topic}</h2>
            <span className={styles.difficulty} style={{ color: getDifficultyColor(quiz.difficulty) }}>
              {quiz.difficulty}
            </span>
          </div>
          <div className={styles.quizMeta}>
            <div className={styles.timer}>
              ⏱️ {formatTime(timeLeft)}
            </div>
            <div className={styles.questionCounter}>
              {currentQuestion + 1} / {quiz.questions.length}
            </div>
          </div>
        </div>

        <div className={styles.progressContainer}>
          <div className={styles.progressBar}>
            <div 
              className={styles.progressFill} 
              style={{ width: `${progress}%` }}
            ></div>
          </div>
        </div>

        <div className={styles.questionCard}>
          <div className={styles.questionHeader}>
            <span className={styles.questionNumber}>Question {currentQuestion + 1}</span>
            <span className={styles.questionType}>{question.type.toUpperCase()}</span>
          </div>
          
          <div className={styles.questionText}>
            {question.question}
          </div>

          {question.type === 'mcq' && (
            <div className={styles.optionsContainer}>
              {question.options.map((option, index) => (
                <label key={index} className={styles.optionLabel}>
                  <input
                    type="radio"
                    name={`question-${currentQuestion}`}
                    value={index}
                    checked={answers[currentQuestion] === index}
                    onChange={() => handleAnswerChange(index)}
                    className={styles.optionRadio}
                  />
                  <span className={styles.optionText}>{option}</span>
                </label>
              ))}
            </div>
          )}

          {question.type === 'coding' && (
            <div className={styles.codingContainer}>
              <textarea
                className={styles.codeTextarea}
                placeholder="Write your code here..."
                value={answers[currentQuestion] || ''}
                onChange={(e) => handleAnswerChange(e.target.value)}
              />
            </div>
          )}
        </div>

        <div className={styles.navigationButtons}>
          <button
            className={styles.navBtn}
            onClick={previousQuestion}
            disabled={currentQuestion === 0}
          >
            ← Previous
          </button>
          
          {currentQuestion === quiz.questions.length - 1 ? (
            <button
              className={styles.submitBtn}
              onClick={handleSubmitQuiz}
            >
              Submit Quiz
            </button>
          ) : (
            <button
              className={styles.navBtn}
              onClick={nextQuestion}
            >
              Next →
            </button>
          )}
        </div>
      </div>
    );
  }

  // Results Phase
  if (phase === 'results' && quizResults) {
    return (
      <div className={styles.container}>
        <div className={styles.resultsCard}>
          <div className={styles.resultsHeader}>
            <h2>Quiz Results</h2>
            <div className={styles.scoreDisplay}>
              <div className={styles.mainScore}>
                {quizResults.score} / {quizResults.total_questions}
              </div>
              <div className={styles.percentage}>
                {quizResults.percentage}%
              </div>
              <div className={`${styles.passStatus} ${quizResults.passed ? styles.passed : styles.failed}`}>
                {quizResults.passed ? '✅ Passed' : '❌ Failed'}
              </div>
            </div>
          </div>

          <div className={styles.performanceSection}>
            <h3>Performance: {quizResults.performance_level}</h3>
            <div className={styles.recommendations}>
              <h4>Recommendations:</h4>
              <ul>
                {quizResults.recommendations.map((rec, index) => (
                  <li key={index}>{rec}</li>
                ))}
              </ul>
            </div>
          </div>

          <div className={styles.detailedResults}>
            <h3>Question Review:</h3>
            {quizResults.detailed_results.map((result, index) => (
              <div key={index} className={`${styles.questionResult} ${result.is_correct ? styles.correct : styles.incorrect}`}>
                <div className={styles.questionResultHeader}>
                  <span>Question {result.question_number}</span>
                  <span className={styles.resultIcon}>
                    {result.is_correct ? '✅' : '❌'}
                  </span>
                </div>
                <div className={styles.questionResultText}>
                  {result.question}
                </div>
                {result.options && (
                  <div className={styles.answerComparison}>
                    <div>Your answer: {result.options[result.user_answer]}</div>
                    <div>Correct answer: {result.options[result.correct_answer]}</div>
                  </div>
                )}
                <div className={styles.explanation}>
                  <strong>Explanation:</strong> {result.explanation}
                </div>
              </div>
            ))}
          </div>

          <div className={styles.resultsActions}>
            <button
              className={styles.actionBtn}
              onClick={restartQuiz}
            >
              Take Quiz Again
            </button>
            <Link
              to={`/tutor/${language}/${encodeURIComponent(topic)}`}
              className={styles.actionBtn}
            >
              Review Tutorial
            </Link>
            <Link
              to="/dashboard"
              className={styles.actionBtn}
            >
              Back to Dashboard
            </Link>
          </div>
        </div>
      </div>
    );
  }

  // Loading state
  return (
    <div className={styles.container}>
      <div className={styles.loadingCard}>
        <div className={styles.spinner}></div>
        <p>Loading quiz...</p>
      </div>
    </div>
  );
};

export default QuizInterface;
