import React from 'react';
import { useLocation, Link } from 'react-router-dom';
import styles from './QuizResults.module.css';

const QuizResults = () => {
  const location = useLocation();
  const { results, language, topic, difficulty } = location.state || {};

  if (!results) {
    return (
      <div className={styles.errorContainer}>
        <div className="error-message">
          No quiz results found. Please take a quiz first.
        </div>
        <Link to="/dashboard" className="btn btn-primary">
          Back to Dashboard
        </Link>
      </div>
    );
  }

  const getScoreColor = (score) => {
    if (score >= 80) return styles.excellent;
    if (score >= 60) return styles.good;
    if (score >= 40) return styles.fair;
    return styles.poor;
  };

  const getScoreMessage = (score) => {
    if (score >= 80) return "Excellent work! 🎉";
    if (score >= 60) return "Good job! 👍";
    if (score >= 40) return "Not bad, but you can do better! 📚";
    return "Keep studying and try again! 💪";
  };

  return (
    <div className={styles.resultsContainer}>
      <div className="page-container">
        <header className={styles.header}>
          <h1>Quiz Results</h1>
          <div className={styles.quizInfo}>
            <span>{language} - {topic}</span>
            <span className={styles.difficulty}>Difficulty: {difficulty}</span>
          </div>
        </header>

        <section className={styles.scoreSection}>
          <div className={`${styles.scoreCard} ${getScoreColor(results.score)}`}>
            <div className={styles.scoreDisplay}>
              <span className={styles.scoreNumber}>{results.score}%</span>
              <span className={styles.scoreText}>
                {results.correct_answers} out of {results.total_questions} correct
              </span>
            </div>
            <p className={styles.scoreMessage}>
              {getScoreMessage(results.score)}
            </p>
            <div className={styles.passFail}>
              {results.passed ? (
                <span className={styles.passed}>✅ Passed</span>
              ) : (
                <span className={styles.failed}>❌ Failed (60% required to pass)</span>
              )}
            </div>
          </div>
        </section>

        <section className={styles.detailsSection}>
          <h2>Question Review</h2>
          <div className={styles.questionsList}>
            {results.results?.map((result, index) => (
              <div key={index} className={styles.questionResult}>
                <div className={styles.questionHeader}>
                  <h3>Question {index + 1}</h3>
                  <span className={`${styles.resultIcon} ${
                    result.is_correct ? styles.correct : styles.incorrect
                  }`}>
                    {result.is_correct ? '✅' : '❌'}
                  </span>
                </div>
                
                <p className={styles.questionText}>
                  {result.question}
                </p>
                
                <div className={styles.answerComparison}>
                  <div className={styles.answerBlock}>
                    <h4>Your Answer:</h4>
                    <p className={styles.userAnswer}>
                      {typeof result.user_answer === 'number' 
                        ? `Option ${String.fromCharCode(65 + result.user_answer)}`
                        : result.user_answer || 'No answer provided'
                      }
                    </p>
                  </div>
                  
                  <div className={styles.answerBlock}>
                    <h4>Correct Answer:</h4>
                    <p className={styles.correctAnswer}>
                      {typeof result.correct_answer === 'number'
                        ? `Option ${String.fromCharCode(65 + result.correct_answer)}`
                        : result.correct_answer
                      }
                    </p>
                  </div>
                </div>
                
                {result.explanation && (
                  <div className={styles.explanation}>
                    <h4>Explanation:</h4>
                    <p>{result.explanation}</p>
                  </div>
                )}
              </div>
            ))}
          </div>
        </section>

        <section className={styles.actionsSection}>
          <div className={styles.actions}>
            <Link 
              to={`/notes/${language}/${encodeURIComponent(topic)}`}
              className="btn btn-secondary"
            >
              📝 Review Notes
            </Link>
            
            <Link 
              to={`/quiz/${language}/${encodeURIComponent(topic)}`}
              className="btn btn-primary"
            >
              🔄 Retake Quiz
            </Link>
            
            <Link 
              to={`/tutor/${language}/${encodeURIComponent(topic)}`}
              className="btn btn-secondary"
            >
              🎓 Review Lesson
            </Link>
            
            <Link 
              to="/dashboard"
              className="btn btn-success"
            >
              🏠 Dashboard
            </Link>
          </div>
        </section>
      </div>
    </div>
  );
};

export default QuizResults;
