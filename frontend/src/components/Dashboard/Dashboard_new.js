import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import apiService from '../../utils/api';
import styles from './Dashboard.module.css';

const Dashboard = () => {
  const { user } = useAuth();
  const [selectedLanguage, setSelectedLanguage] = useState(null);
  const [topicsData, setTopicsData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const languages = [
    { 
      name: 'Python', 
      icon: '🐍', 
      description: 'Data science, AI, and web development',
      color: '#3776ab'
    },
    { 
      name: 'Java', 
      icon: '☕', 
      description: 'Enterprise applications and Android development',
      color: '#f89820'
    },
    { 
      name: 'C', 
      icon: '🔧', 
      description: 'System programming and embedded systems',
      color: '#659ad2'
    },
    { 
      name: 'JavaScript', 
      icon: '🌐', 
      description: 'Web development and interactive applications',
      color: '#f7df1e'
    }
  ];

  const fetchTopicsForLanguage = async (language) => {
    try {
      setLoading(true);
      setError('');
      const response = await apiService.getTopicsWithProgress(language);
      setTopicsData(response);
    } catch (error) {
      setError('Failed to load topics data');
      console.error('Error fetching topics:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLanguageSelect = (language) => {
    setSelectedLanguage(language);
    fetchTopicsForLanguage(language.name);
  };

  const getTopicStatus = (topic) => {
    if (!topic.is_unlocked) return 'locked';
    if (topic.completed) return 'completed';
    if (topic.tutorial_completed || topic.quiz_attempts > 0) return 'in-progress';
    return 'available';
  };

  const getStatusColor = (status) => {
    const colors = {
      'completed': '#4CAF50',
      'in-progress': '#FF9800',
      'available': '#2196F3',
      'locked': '#9E9E9E'
    };
    return colors[status] || '#9E9E9E';
  };

  const getStatusIcon = (status) => {
    const icons = {
      'completed': '✅',
      'in-progress': '📚',
      'available': '🚀',
      'locked': '🔒'
    };
    return icons[status] || '📖';
  };

  const calculateLanguageProgress = (topics) => {
    if (!topics || topics.length === 0) return 0;
    const completed = topics.filter(t => t.completed).length;
    return Math.round((completed / topics.length) * 100);
  };

  if (!selectedLanguage) {
    return (
      <div className={styles.container}>
        <div className={styles.header}>
          <h1 className={styles.title}>Welcome back, {user?.username}!</h1>
          <p className={styles.subtitle}>Choose a programming language to continue your learning journey</p>
        </div>

        <div className={styles.languageGrid}>
          {languages.map((language) => (
            <div
              key={language.name}
              className={styles.languageCard}
              onClick={() => handleLanguageSelect(language)}
              style={{ borderColor: language.color }}
            >
              <div className={styles.languageIcon} style={{ backgroundColor: language.color }}>
                {language.icon}
              </div>
              <div className={styles.languageInfo}>
                <h3 className={styles.languageName}>{language.name}</h3>
                <p className={styles.languageDescription}>{language.description}</p>
              </div>
              <div className={styles.languageAction}>
                <span className={styles.startButton}>Start Learning →</span>
              </div>
            </div>
          ))}
        </div>

        <div className={styles.featuresSection}>
          <h2>What you'll learn:</h2>
          <div className={styles.features}>
            <div className={styles.feature}>
              <span className={styles.featureIcon}>📚</span>
              <div>
                <h4>Interactive Tutorials</h4>
                <p>Step-by-step lessons with hands-on examples</p>
              </div>
            </div>
            <div className={styles.feature}>
              <span className={styles.featureIcon}>🧪</span>
              <div>
                <h4>Practice Quizzes</h4>
                <p>Test your knowledge with AI-generated questions</p>
              </div>
            </div>
            <div className={styles.feature}>
              <span className={styles.featureIcon}>💻</span>
              <div>
                <h4>Code Practice</h4>
                <p>Write and run code directly in your browser</p>
              </div>
            </div>
            <div className={styles.feature}>
              <span className={styles.featureIcon}>🏆</span>
              <div>
                <h4>Progressive Learning</h4>
                <p>Unlock topics as you master the fundamentals</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <button 
          className={styles.backButton}
          onClick={() => {
            setSelectedLanguage(null);
            setTopicsData(null);
          }}
        >
          ← Back to Languages
        </button>
        <div className={styles.languageHeader}>
          <span 
            className={styles.currentLanguageIcon}
            style={{ backgroundColor: selectedLanguage.color }}
          >
            {selectedLanguage.icon}
          </span>
          <div>
            <h1 className={styles.title}>{selectedLanguage.name} Learning Path</h1>
            {topicsData && (
              <p className={styles.progressSummary}>
                Progress: {calculateLanguageProgress(topicsData.topics)}% • 
                {topicsData.total_completed} of {topicsData.topics.length} topics completed
              </p>
            )}
          </div>
        </div>
      </div>

      {loading ? (
        <div className={styles.loading}>
          <div className={styles.spinner}></div>
          <p>Loading learning path...</p>
        </div>
      ) : error ? (
        <div className={styles.error}>
          <p>{error}</p>
          <button onClick={() => fetchTopicsForLanguage(selectedLanguage.name)}>
            Try Again
          </button>
        </div>
      ) : topicsData ? (
        <div className={styles.topicsContainer}>
          <div className={styles.progressBar}>
            <div 
              className={styles.progressFill}
              style={{ 
                width: `${calculateLanguageProgress(topicsData.topics)}%`,
                backgroundColor: selectedLanguage.color
              }}
            ></div>
          </div>

          <div className={styles.topicsGrid}>
            {topicsData.topics.map((topic) => {
              const status = getTopicStatus(topic);
              const isAccessible = status !== 'locked';

              return (
                <div
                  key={topic.topic}
                  className={`${styles.topicCard} ${styles[status]} ${!isAccessible ? styles.disabled : ''}`}
                  style={{
                    borderColor: getStatusColor(status),
                    opacity: isAccessible ? 1 : 0.6
                  }}
                >
                  <div className={styles.topicHeader}>
                    <div className={styles.topicLevel}>
                      Level {topic.level}
                    </div>
                    <div className={styles.topicStatus}>
                      {getStatusIcon(status)}
                    </div>
                  </div>

                  <div className={styles.topicContent}>
                    <h3 className={styles.topicTitle}>{topic.topic}</h3>
                    <p className={styles.topicDescription}>{topic.description}</p>

                    {topic.prerequisites.length > 0 && (
                      <div className={styles.prerequisites}>
                        <small>Prerequisites: {topic.prerequisites.join(', ')}</small>
                      </div>
                    )}

                    {topic.quiz_attempts > 0 && (
                      <div className={styles.topicStats}>
                        <span>Quiz attempts: {topic.quiz_attempts}</span>
                        <span>Best score: {topic.best_quiz_score}%</span>
                      </div>
                    )}
                  </div>

                  <div className={styles.topicActions}>
                    {!isAccessible ? (
                      <div className={styles.lockedMessage}>
                        <span>🔒 Complete previous topics to unlock</span>
                      </div>
                    ) : (
                      <>
                        <Link
                          to={`/tutor/${selectedLanguage.name}/${encodeURIComponent(topic.topic)}`}
                          className={`${styles.actionButton} ${styles.tutorialButton}`}
                        >
                          {topic.tutorial_completed ? '📖 Review Tutorial' : '🎯 Start Tutorial'}
                        </Link>
                        
                        <Link
                          to={`/quiz/${selectedLanguage.name}/${encodeURIComponent(topic.topic)}`}
                          className={`${styles.actionButton} ${styles.quizButton}`}
                          style={{ backgroundColor: selectedLanguage.color }}
                        >
                          {topic.quiz_attempts > 0 ? '🔄 Retake Quiz' : '🧪 Take Quiz'}
                        </Link>
                      </>
                    )}
                  </div>
                </div>
              );
            })}
          </div>

          <div className={styles.helpSection}>
            <h3>Need Help?</h3>
            <div className={styles.helpContent}>
              <div className={styles.helpItem}>
                <strong>🎯 Start with tutorials:</strong> Learn concepts step by step
              </div>
              <div className={styles.helpItem}>
                <strong>🧪 Practice with quizzes:</strong> Test your understanding
              </div>
              <div className={styles.helpItem}>
                <strong>🔒 Unlock new topics:</strong> Complete previous levels to progress
              </div>
              <div className={styles.helpItem}>
                <strong>🔄 Review anytime:</strong> Revisit completed topics to reinforce learning
              </div>
            </div>
          </div>
        </div>
      ) : null}
    </div>
  );
};

export default Dashboard;
