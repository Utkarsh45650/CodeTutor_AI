import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './context/AuthContext';
import { useTheme } from './context/ThemeContext';
import Header from './components/Common/Header';
import Login from './components/Auth/Login';
import Register from './components/Auth/Register';
import Dashboard from './components/Dashboard/Dashboard';
import TutorInterface from './components/Tutor/TutorInterface';
import QuizInterface from './components/Quiz/QuizInterface';
import QuizResults from './components/Quiz/QuizResults';
import CustomQuiz from './components/Quiz/CustomQuiz';
import Notes from './components/Tutor/Notes';
import './App.css';

function App() {
  const { user } = useAuth();
  const { theme } = useTheme();

  return (
    <div className="App" data-theme={theme}>
      <Router>
        {user && <Header />}
        <main className="main-content">
          <Routes>
            {!user ? (
              <>
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route path="*" element={<Navigate to="/login" />} />
              </>
            ) : (
              <>
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/tutor/:language/:topic" element={<TutorInterface />} />
                <Route path="/notes/:language/:topic" element={<Notes />} />
                <Route path="/quiz/:language/:topic" element={<QuizInterface />} />
                <Route path="/quiz-results" element={<QuizResults />} />
                <Route path="/custom-quiz/:language" element={<CustomQuiz />} />
                <Route path="*" element={<Navigate to="/dashboard" />} />
              </>
            )}
          </Routes>
        </main>
      </Router>
    </div>
  );
}

export default App;
