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
      const response = await apiService.getTutorContent(language, topic);
      setContent(response);
    } catch (error) {
      setError('Failed to load tutorial content');
    } finally {
      setLoading(false);
    }
  }, [language, topic]);

  useEffect(() => {
    fetchTutorContent();
  }, [fetchTutorContent]);

  const handleNext = () => {
    if (currentStep < content.content.length - 1) {
      setCurrentStep(currentStep + 1);
    } else if (currentStep < content.content.length + content.checkpoints.length - 1) {
      // Move to checkpoint
      setCurrentStep(currentStep + 1);
    } else {
      // Completed the lesson
      markAsCompleted();
    }
  };

  const handleCheckpointResponse = (response) => {
    const newResponses = [...checkpointResponses];
    const checkpointIndex = currentStep - content.content.length;
    newResponses[checkpointIndex] = response;
    setCheckpointResponses(newResponses);
    
    if (response === 'yes') {
      handleNext();
    } else {
      // If user says no, go back to explain more or stay on current step
      alert("No problem! Take your time to understand the concept. You can review the notes or ask for clarification.");
    }
  };

  const markAsCompleted = async () => {
    try {
      await apiService.updateProgress(language, topic);
      setIsCompleted(true);
    } catch (error) {
      console.error('Failed to update progress:', error);
      setIsCompleted(true); // Still show completion even if progress update fails
    }
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
        </div>

        <div className={styles.mainContent}>
          <div className={styles.contentHeader}>
            <h2>Interactive Tutorial</h2>
            <p>Learn at your own pace with AI-powered guidance</p>
          </div>

        <main className={styles.content}>
          <div className={styles.tutorCard}>
            <div className={styles.tutorAvatar}>
              <span>🤖</span>
            </div>
            
            <div className={styles.messageContainer}>
              <h3 className={styles.messageTitle}>
                {currentContent?.type === 'checkpoint' ? 'Quick Check!' : 'AI Tutor'}
              </h3>
              
              <p className={styles.messageText}>
                {currentContent?.text}
              </p>
              
              {currentContent?.type === 'checkpoint' ? (
                <div className={styles.checkpointActions}>
                  <button 
                    onClick={() => handleCheckpointResponse('yes')}
                    className="btn btn-success"
                  >
                    Yes, I understand! ✓
                  </button>
                  <button 
                    onClick={() => handleCheckpointResponse('no')}
                    className="btn btn-secondary"
                  >
                    I need more explanation 🤔
                  </button>
                </div>
              ) : (
                <div className={styles.contentActions}>
                  <button 
                    onClick={handleNext}
                    className="btn btn-primary"
                  >
                    {currentStep === content.content.length - 1 ? 
                      'Continue to Checkpoint' : 
                      'Next →'
                    }
                  </button>
                </div>
              )}
            </div>
          </div>
        </main>

        <aside className={styles.sidebar}>
          <Link 
            to={`/notes/${language}/${encodeURIComponent(topic)}`}
            className="btn btn-secondary w-full"
          >
            📝 View Notes
          </Link>
          
          <div className={styles.helpSection}>
            <h4>Need Help?</h4>
            <p>
              Take your time to understand each concept. The AI tutor will guide you through step by step.
            </p>
          </div>
        </aside>
      </div>
    </div>
  );
};

export default TutorInterface;
