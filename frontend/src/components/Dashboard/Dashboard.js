import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import apiService from '../../utils/api';
import styles from './Dashboard.module.css';

const Dashboard = () => {
  const { user } = useAuth();
  const [progress, setProgress] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const languages = [
    { name: 'C', icon: '🔧', description: 'System programming and embedded systems' },
    { name: 'C++', icon: '⚡', description: 'Object-oriented programming and game development' },
    { name: 'C#', icon: '🎯', description: 'Modern applications and web development' },
    { name: 'Java', icon: '☕', description: 'Enterprise applications and Android development' },
    { name: 'Python', icon: '🐍', description: 'Data science, AI, and web development' }
  ];

  useEffect(() => {
    fetchUserProgress();
  }, []);

  const fetchUserProgress = async () => {
    try {
      const userProgress = await apiService.getUserProgress();
      setProgress(userProgress);
    } catch (error) {
      setError('Failed to load progress data');
    } finally {
      setLoading(false);
    }
  };

  const getLanguageProgress = (language) => {
    const languageData = progress[language];
    if (!languageData) return { completed: 0, total: 4, percentage: 0 };
    
    const completed = languageData.completed_topics?.length || 0;
    const total = 4; // Assuming 4 topics per language
    const percentage = total > 0 ? (completed / total) * 100 : 0;
    
    return { completed, total, percentage };
  };

  const getOverallProgress = () => {
    let totalCompleted = 0;
    let totalTopics = 0;
    
    languages.forEach(lang => {
      const langProgress = getLanguageProgress(lang.name);
      totalCompleted += langProgress.completed;
      totalTopics += langProgress.total;
    });
    
    return totalTopics > 0 ? (totalCompleted / totalTopics) * 100 : 0;
  };

  const hasCompletedEnoughTopics = (language) => {
    const langProgress = getLanguageProgress(language);
    return langProgress.completed >= 4; // Need 4 completed topics for custom quiz
  };

  if (loading) {
    return (
      <div className={styles.loadingContainer}>
        <div className="loading-spinner"></div>
        <p>Loading your progress...</p>
      </div>
    );
  }

  return (
    <div className={styles.dashboard}>
      <div className="page-container">
        <header className={styles.header}>
          <h1>Welcome back, {user.username}! 👋</h1>
          <p className={styles.subtitle}>
            Continue your programming journey or start a new topic
          </p>
        </header>

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        <section className={styles.progressSection}>
          <h2>Overall Progress</h2>
          <div className={styles.progressBar}>
            <div 
              className={styles.progressFill}
              style={{ width: `${getOverallProgress()}%` }}
            ></div>
          </div>
          <p className={styles.progressText}>
            {getOverallProgress().toFixed(1)}% Complete
          </p>
        </section>

        <section className={styles.languagesSection}>
          <h2>Programming Languages</h2>
          <div className="grid grid-2">
            {languages.map(language => {
              const languageProgress = getLanguageProgress(language.name);
              return (
                <div key={language.name} className={`card ${styles.languageCard}`}>
                  <div className={styles.languageHeader}>
                    <span className={styles.languageIcon}>{language.icon}</span>
                    <h3>{language.name}</h3>
                  </div>
                  
                  <p className={styles.languageDescription}>
                    {language.description}
                  </p>
                  
                  <div className={styles.languageProgress}>
                    <div className={styles.progressBar}>
                      <div 
                        className={styles.progressFill}
                        style={{ width: `${languageProgress.percentage}%` }}
                      ></div>
                    </div>
                    <span className={styles.progressText}>
                      {languageProgress.completed}/{languageProgress.total} topics
                    </span>
                  </div>
                  
                  <div className={styles.languageActions}>
                    <Link 
                      to={`/tutor/${language.name}/Variables and Data Types`}
                      className="btn btn-primary"
                    >
                      Start Learning
                    </Link>
                    
                    {hasCompletedEnoughTopics(language.name) && (
                      <Link 
                        to={`/custom-quiz/${language.name}`}
                        className="btn btn-secondary"
                      >
                        Custom Quiz
                      </Link>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </section>

        <section className={styles.statsSection}>
          <h2>Your Statistics</h2>
          <div className="grid grid-3">
            <div className={`card ${styles.statCard}`}>
              <h3>Topics Completed</h3>
              <p className={styles.statNumber}>
                {Object.values(progress).reduce((total, lang) => 
                  total + (lang.completed_topics?.length || 0), 0
                )}
              </p>
            </div>
            
            <div className={`card ${styles.statCard}`}>
              <h3>Quizzes Taken</h3>
              <p className={styles.statNumber}>
                {Object.values(progress).reduce((total, lang) => 
                  total + Object.keys(lang.quiz_scores || {}).length, 0
                )}
              </p>
            </div>
            
            <div className={`card ${styles.statCard}`}>
              <h3>Average Score</h3>
              <p className={styles.statNumber}>
                {(() => {
                  const allScores = [];
                  Object.values(progress).forEach(lang => {
                    if (lang.quiz_scores) {
                      allScores.push(...Object.values(lang.quiz_scores));
                    }
                  });
                  return allScores.length > 0 
                    ? Math.round(allScores.reduce((a, b) => a + b, 0) / allScores.length) + '%'
                    : 'No quizzes yet';
                })()}
              </p>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
};

export default Dashboard;
