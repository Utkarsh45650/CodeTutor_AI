import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import apiService from '../../utils/api';
import styles from './Notes.module.css';

const Notes = () => {
  const { language, topic } = useParams();
  const [notes, setNotes] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchNotes();
  }, [language, topic]);

  const fetchNotes = async () => {
    try {
      setLoading(true);
      const response = await apiService.getTopicNotes(language, topic);
      setNotes(response.notes);
    } catch (error) {
      setError('Failed to load notes');
    } finally {
      setLoading(false);
    }
  };

  const renderMarkdown = (text) => {
    // Simple markdown rendering for headers, code blocks, and basic formatting
    return text
      .replace(/^# (.*$)/gm, '<h1>$1</h1>')
      .replace(/^## (.*$)/gm, '<h2>$1</h2>')
      .replace(/^### (.*$)/gm, '<h3>$1</h3>')
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>')
      .replace(/`(.*?)`/g, '<code>$1</code>')
      .replace(/\n/g, '<br>');
  };

  if (loading) {
    return (
      <div className={styles.loadingContainer}>
        <div className="loading-spinner"></div>
        <p>Loading notes...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className={styles.errorContainer}>
        <div className="error-message">
          {error}
        </div>
        <Link to="/dashboard" className="btn btn-primary">
          Back to Dashboard
        </Link>
      </div>
    );
  }

  return (
    <div className={styles.notesContainer}>
      <div className="page-container">
        <header className={styles.header}>
          <div className={styles.breadcrumb}>
            <Link to="/dashboard">Dashboard</Link>
            <span>→</span>
            <Link to={`/tutor/${language}/${encodeURIComponent(topic)}`}>
              {language}
            </Link>
            <span>→</span>
            <span>Notes: {topic}</span>
          </div>
          
          <h1 className={styles.title}>
            📝 {topic} - {language}
          </h1>
        </header>

        <div className={styles.content}>
          <main className={styles.notesContent}>
            <div className={styles.notesCard}>
              <div 
                className={styles.markdownContent}
                dangerouslySetInnerHTML={{ __html: renderMarkdown(notes) }}
              />
            </div>
          </main>

          <aside className={styles.sidebar}>
            <div className={styles.actionCard}>
              <h3>Quick Actions</h3>
              <div className={styles.actions}>
                <Link 
                  to={`/tutor/${language}/${encodeURIComponent(topic)}`}
                  className="btn btn-primary w-full"
                >
                  🎓 Back to Lesson
                </Link>
                <Link 
                  to={`/quiz/${language}/${encodeURIComponent(topic)}`}
                  className="btn btn-success w-full"
                >
                  🎯 Take Quiz
                </Link>
                <Link 
                  to="/dashboard"
                  className="btn btn-secondary w-full"
                >
                  🏠 Dashboard
                </Link>
              </div>
            </div>

            <div className={styles.tipCard}>
              <h4>Study Tips</h4>
              <ul>
                <li>Read through the notes completely</li>
                <li>Try to understand the examples</li>
                <li>Practice writing code based on the concepts</li>
                <li>Take the quiz to test your understanding</li>
              </ul>
            </div>
          </aside>
        </div>
      </div>
    </div>
  );
};

export default Notes;
