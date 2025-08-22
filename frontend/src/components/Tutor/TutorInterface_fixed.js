import React, { useState, useEffect, useCallback } from 'react';
import { useParams, Link } from 'react-router-dom';
import apiService from '../../utils/api';
import styles from './TutorInterface_enhanced.module.css';

const TutorInterface = () => {
  const { language, topic } = useParams();
  const [content, setContent] = useState(null);
  const [currentStep, setCurrentStep] = useState(0);
  const [checkpointResponses, setCheckpointResponses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [isCompleted, setIsCompleted] = useState(false);

  const fetchTutorContent = useCallback(async () => {
    try {
      setLoading(true);
      setError('');
      const response = await apiService.getTutorContent(language, topic);
      setContent(response);
    } catch (error) {
      console.error('Error fetching tutor content:', error);
      setError('Failed to load tutorial content. Please check your internet connection and try again.');
    } finally {
      setLoading(false);
    }
  }, [language, topic]);

  useEffect(() => {
    fetchTutorContent();
  }, [fetchTutorContent]);

  const handleNext = () => {
    const totalSteps = content.content.length + content.checkpoints.length;
    if (currentStep < totalSteps - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      setIsCompleted(true);
    }
  };

  const handleCheckpointResponse = (response) => {
    const newResponses = [...checkpointResponses, response];
    setCheckpointResponses(newResponses);
    
    if (response === 'no') {
      // For now, just continue to next step
      // In a real implementation, you might show additional explanation
    }
    
    handleNext();
  };

  const getCurrentContent = () => {
    if (!content) return null;
    
    if (currentStep < content.content.length) {
      return {
        type: 'content',
        text: content.content[currentStep]
      };
    } else {
      const checkpointIndex = currentStep - content.content.length;
      if (checkpointIndex < content.checkpoints.length) {
        return {
          type: 'checkpoint',
          text: content.checkpoints[checkpointIndex]
        };
      }
    }
    return null;
  };

  if (loading) {
    return (
      <div className={styles.container}>
        <div className={styles.header}>
          <Link to="/dashboard" className={styles.backLink}>
            ← Back to Dashboard
          </Link>
          <h1 className={styles.title}>AI Tutor</h1>
        </div>
        
        <div className={styles.loading}>
          <div className={styles.loadingSpinner}></div>
          <div className={styles.loadingText}>Loading tutorial content...</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={styles.container}>
        <div className={styles.header}>
          <Link to="/dashboard" className={styles.backLink}>
            ← Back to Dashboard
          </Link>
          <h1 className={styles.title}>Tutorial Error</h1>
        </div>
        
        <div className={styles.error}>
          <h2>😔 Oops! Something went wrong</h2>
          <p>{error}</p>
          <div style={{ display: 'flex', gap: '15px', justifyContent: 'center', marginTop: '20px' }}>
            <button 
              onClick={() => {
                setError('');
                fetchTutorContent();
              }}
              className={styles.retryButton}
            >
              Try Again
            </button>
            <Link to="/dashboard" className={styles.actionBtn}>
              Back to Dashboard
            </Link>
          </div>
        </div>
      </div>
    );
  }

  if (isCompleted) {
    return (
      <div className={styles.container}>
        <div className={styles.header}>
          <Link to="/dashboard" className={styles.backLink}>
            ← Back to Dashboard
          </Link>
          <h1 className={styles.title}>Lesson Complete!</h1>
        </div>
        
        <div className={styles.resultsCard}>
          <div className={styles.resultsHeader}>
            <h2>🎉 Lesson Completed!</h2>
            <p>Great job! You've completed the lesson on <strong>{topic}</strong> in {language}.</p>
            <p>You can now take a quiz to test your understanding or view your notes.</p>
          </div>
          
          <div className={styles.resultsActions}>
            <Link 
              to={`/quiz/${language}/${encodeURIComponent(topic)}`}
              className={styles.actionBtn}
            >
              🎯 Take Quiz
            </Link>
            <Link 
              to="/dashboard"
              className={styles.actionBtn}
            >
              🏠 Dashboard
            </Link>
          </div>
        </div>
      </div>
    );
  }

  const currentContent = getCurrentContent();
  const totalSteps = content.content.length + content.checkpoints.length;
  const progress = ((currentStep + 1) / totalSteps) * 100;

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <Link to="/dashboard" className={styles.backLink}>
          ← Back to Dashboard
        </Link>
        <h1 className={styles.title}>AI Tutor - {topic}</h1>
      </div>

      <div className={styles.content}>
        <div className={styles.sidebar}>
          <div className={styles.sidebarHeader}>
            <h2>Learning Progress</h2>
          </div>
          
          <div className={styles.topicInfo}>
            <div className={styles.topicName}>{topic}</div>
            <div className={styles.difficultyLevel}>{language}</div>
          </div>

          <div className={styles.progressContainer}>
            <div className={styles.progressBar}>
              <div 
                className={styles.progressFill}
                style={{ width: `${progress}%` }}
              ></div>
            </div>
            <div style={{ textAlign: 'center', marginTop: '10px', color: '#666' }}>
              Step {currentStep + 1} of {totalSteps}
            </div>
          </div>

          <div className={styles.quickActions}>
            <Link 
              to={`/quiz/${language}/${encodeURIComponent(topic)}`}
              className={styles.quickActionBtn}
            >
              🎯 Take Quiz
            </Link>
          </div>
        </div>

        <div className={styles.mainContent}>
          <div className={styles.contentHeader}>
            <h2>Interactive Tutorial</h2>
            <p>Learn at your own pace with AI-powered guidance</p>
          </div>

          <div className={styles.chatContainer}>
            <div className={styles.messageWrapper}>
              <div className={styles.avatar} style={{ background: 'linear-gradient(45deg, #4CAF50, #45a049)' }}>
                🤖
              </div>
              <div className={styles.messageContent} style={{ background: 'white', color: '#333' }}>
                <h3 style={{ marginTop: 0, marginBottom: '15px', color: '#4CAF50' }}>
                  {currentContent?.type === 'checkpoint' ? 'Quick Check!' : 'AI Tutor'}
                </h3>
                <div dangerouslySetInnerHTML={{ __html: currentContent?.text }}></div>
              </div>
            </div>
          </div>
          
          <div className={styles.inputSection}>
            {currentContent?.type === 'checkpoint' ? (
              <div className={styles.inputOptions}>
                <div className={styles.quickActions}>
                  <button 
                    onClick={() => handleCheckpointResponse('yes')}
                    className={styles.quickActionBtn}
                    style={{ backgroundColor: '#4CAF50', color: 'white', border: '2px solid #4CAF50' }}
                  >
                    Yes, I understand! ✓
                  </button>
                  <button 
                    onClick={() => handleCheckpointResponse('no')}
                    className={styles.quickActionBtn}
                  >
                    I need more explanation 🤔
                  </button>
                </div>
              </div>
            ) : (
              <div className={styles.inputOptions}>
                <div className={styles.quickActions}>
                  <button 
                    onClick={handleNext}
                    className={styles.quickActionBtn}
                    style={{ backgroundColor: '#667eea', color: 'white', border: '2px solid #667eea' }}
                  >
                    {currentStep === content.content.length - 1 ? 
                      'Continue to Checkpoint →' : 
                      'Next →'
                    }
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default TutorInterface;
