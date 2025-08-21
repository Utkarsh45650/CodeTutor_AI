import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import ThemeToggle from './ThemeToggle';
import styles from './Header.module.css';

const Header = () => {
  const { user, logout } = useAuth();
  const location = useLocation();

  const isActive = (path) => {
    return location.pathname === path;
  };

  return (
    <header className={styles.header}>
      <div className={styles.container}>
        <Link to="/dashboard" className={styles.logo}>
          <span className={styles.logoIcon}>🎓</span>
          CodeTutor AI
        </Link>

        <nav className={styles.nav}>
          <Link 
            to="/dashboard" 
            className={`${styles.navLink} ${isActive('/dashboard') ? styles.active : ''}`}
          >
            Dashboard
          </Link>
        </nav>

        <div className={styles.userActions}>
          <ThemeToggle />
          
          <div className={styles.userInfo}>
            <span className={styles.username}>
              {user.username}
            </span>
            <button 
              onClick={logout}
              className={`btn btn-secondary ${styles.logoutBtn}`}
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
