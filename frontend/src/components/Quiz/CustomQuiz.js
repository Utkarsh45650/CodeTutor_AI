import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import apiService from '../../utils/api';
import styles from './CustomQuiz.module.css';

const CustomQuiz = () => {
  const { language } = useParams();
  const navigate = useNavigate();
  const [topics, setTopics] = useState([]);
  const [selectedTopics, setSelectedTopics] = useState([]);
  const [progress, setProgress] = useState({});
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchData();
  }, [language]);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [topicsResponse, progressResponse] = await Promise.all([
        apiService.getAvailableTopics(language),
        apiService.getUserProgress()
      ]);
      
      setTopics(topicsResponse.topics);
      setProgress(progressResponse);
    } catch (error) {
      setError('Failed to load data');
    } finally {
      setLoading(false);
    }
  };

  const getCompletedTopics = () => {
    const languageProgress = progress[language];
    if (!languageProgress) return [];
    return languageProgress.completed_topics || [];
  };

  const isTopicCompleted = (topic) => {
    return getCompletedTopics().includes(topic);
  };

  const handleTopicToggle = (topic) => {
    if (!isTopicCompleted(topic)) return;
    
    setSelectedTopics(prev => {
      if (prev.includes(topic)) {
        return prev.filter(t => t !== topic);
      } else {
        return [...prev, topic];
      }
    });
  };

  const generateCustomQuiz = async () => {
    if (selectedTopics.length < 2) {
      alert('Please select at least 2 topics for the custom quiz');
      return;
    }

    try {
      setGenerating(true);
      const response = await apiService.generateCustomQuiz(language, selectedTopics);
      
      // Navigate to quiz interface with custom quiz data
      navigate('/quiz-results', {
        state: {
          quizData: response,
          isCustom: true,
          language,
          selectedTopics
        }
      });
    } catch (error) {
      setError('Failed to generate custom quiz');
    } finally {
      setGenerating(false);
    }
  };

  if (loading) {
    return (
      <div className={styles.loadingContainer}>
        <div className="loading-spinner"></div>
        <p>Loading topics...</p>
      </div>
    );
  }

  const completedTopics = getCompletedTopics();
  const availableTopics = topics.filter(topic => isTopicCompleted(topic));

  if (availableTopics.length < 2) {
    return (
      <div className={styles.insufficientContainer}>
        <div className={styles.insufficientCard}>
          <h2>🚧 Custom Quiz Not Available</h2>
          <p>
            You need to complete at least 4 topics in {language} to unlock the custom quiz feature.
          </p>
          <p>
            Currently completed: <strong>{completedTopics.length}</strong> out of 4 required topics.
          </p>
          
          <div className={styles.topicsList}>
            <h3>Your Progress:</h3>
            {topics.map(topic => (
              <div key={topic} className={styles.topicItem}>
                <span className={isTopicCompleted(topic) ? styles.completed : styles.incomplete}>
                  {isTopicCompleted(topic) ? '✅' : '⏳'}
                </span>
                <span>{topic}</span>
              </div>
            ))}
          </div>
          
          <Link to="/dashboard" className="btn btn-primary">
            Back to Dashboard
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className={styles.customQuizContainer}>
      <div className="page-container">
        <header className={styles.header}>
          <div className={styles.breadcrumb}>
            <Link to="/dashboard">Dashboard</Link>
            <span>→</span>
            <span>Custom Quiz - {language}</span>
          </div>
          
          <h1>🎯 Custom Quiz Generator</h1>
          <p className={styles.subtitle}>
            Create a personalized quiz by selecting topics you've mastered
          </p>
        </header>

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        <section className={styles.selectionSection}>
          <h2>Select Topics (Choose at least 2)</h2>
          <p className={styles.selectionNote}>
            You can only select topics you've completed. The quiz will contain mixed questions from all selected topics.
          </p>
          
          <div className={styles.topicsGrid}>
            {topics.map(topic => {
              const completed = isTopicCompleted(topic);
              const selected = selectedTopics.includes(topic);
              
              return (
                <div
                  key={topic}
                  onClick={() => handleTopicToggle(topic)}
                  className={`${styles.topicCard} ${
                    completed ? styles.available : styles.locked
                  } ${selected ? styles.selected : ''}`}
                >
                  <div className={styles.topicHeader}>
                    <span className={styles.topicIcon}>
                      {completed ? (selected ? '✅' : '📚') : '🔒'}
                    </span>
                    <h3 className={styles.topicTitle}>{topic}</h3>
                  </div>
                  
                  <div className={styles.topicStatus}>
                    {completed ? (
                      <span className={styles.statusCompleted}>
                        ✓ Completed
                      </span>
                    ) : (
                      <span className={styles.statusLocked}>
                        🔒 Not Completed
                      </span>
                    )}
                  </div>
                  
                  {completed && (
                    <div className={styles.quizScore}>
                      Score: {progress[language]?.quiz_scores?.[topic] || 'No quiz taken'}%
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </section>

        {selectedTopics.length > 0 && (
          <section className={styles.summarySection}>
            <div className={styles.summaryCard}>
              <h3>Quiz Summary</h3>
              <div className={styles.summaryDetails}>
                <div className={styles.summaryItem}>
                  <strong>Language:</strong> {language}
                </div>
                <div className={styles.summaryItem}>
                  <strong>Selected Topics:</strong> {selectedTopics.length}
                </div>
                <div className={styles.summaryItem}>
                  <strong>Topics:</strong> {selectedTopics.join(', ')}
                </div>
                <div className={styles.summaryItem}>
                  <strong>Estimated Questions:</strong> ~10 mixed questions
                </div>
                <div className={styles.summaryItem}>
                  <strong>Time Limit:</strong> 20 minutes
                </div>
              </div>
            </div>
          </section>
        )}

        <section className={styles.actionsSection}>
          <div className={styles.actions}>
            <Link to="/dashboard" className="btn btn-secondary">
              Cancel
            </Link>
            
            <button
              onClick={generateCustomQuiz}
              disabled={selectedTopics.length < 2 || generating}
              className="btn btn-primary"
            >
              {generating ? (
                <>
                  <span className="loading-spinner"></span>
                  Generating Quiz...
                </>
              ) : (
                `Generate Custom Quiz (${selectedTopics.length} topics)`
              )}
            </button>
          </div>
        </section>
      </div>
    </div>
  );
};

export default CustomQuiz;
