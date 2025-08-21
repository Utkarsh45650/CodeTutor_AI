import React, { useState } from 'react';
import apiService from '../../utils/api';
import styles from './CodeEditor.module.css';

const CodeEditor = ({ language, onResult }) => {
  const [code, setCode] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleRunCode = async () => {
    if (!code.trim()) {
      alert('Please enter some code to run');
      return;
    }

    setLoading(true);
    try {
      const response = await apiService.runCode(code, language.toLowerCase());
      setResult(response);
      if (onResult) {
        onResult(response);
      }
    } catch (error) {
      setResult({
        success: false,
        output: '',
        error: error.message
      });
    } finally {
      setLoading(false);
    }
  };

  const getPlaceholder = () => {
    const placeholders = {
      'c': `#include <stdio.h>

int main() {
    printf("Hello, World!\\n");
    return 0;
}`,
      'c++': `#include <iostream>
using namespace std;

int main() {
    cout << "Hello, World!" << endl;
    return 0;
}`,
      'java': `public class Main {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}`,
      'python': `print("Hello, World!")`,
      'c#': `using System;

class Program {
    static void Main() {
        Console.WriteLine("Hello, World!");
    }
}`
    };
    
    return placeholders[language.toLowerCase()] || 'Enter your code here...';
  };

  return (
    <div className={styles.codeEditor}>
      <div className={styles.editorHeader}>
        <h3>Code Editor - {language}</h3>
        <button 
          onClick={handleRunCode}
          disabled={loading}
          className="btn btn-primary"
        >
          {loading ? (
            <>
              <span className="loading-spinner"></span>
              Running...
            </>
          ) : (
            '▶️ Run Code'
          )}
        </button>
      </div>

      <textarea
        value={code}
        onChange={(e) => setCode(e.target.value)}
        placeholder={getPlaceholder()}
        className={styles.codeTextarea}
        spellCheck={false}
      />

      {result && (
        <div className={styles.resultSection}>
          <h4>Output:</h4>
          <div className={`${styles.resultBox} ${result.success ? styles.success : styles.error}`}>
            {result.success ? (
              <pre>{result.output || 'Program executed successfully (no output)'}</pre>
            ) : (
              <pre className={styles.errorText}>
                {result.error || 'An error occurred while running the code'}
              </pre>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default CodeEditor;
