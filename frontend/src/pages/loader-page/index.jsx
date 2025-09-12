// LoaderPage.jsx
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./loader-page.css";

const LoaderPage = () => {
  const navigate = useNavigate();
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    let current = 0;
    const interval = setInterval(() => {
      current += 5; // Increase 5% every second
      if (current >= 100) {
        clearInterval(interval);
        // After 20s, go back to dashboard (or repo list)
        navigate("/dashboard"); 
      }
      setProgress(current);
    }, 1000); // 20 steps → 20s

    return () => clearInterval(interval);
  }, [navigate]);

  return (
    <div className="loader-page">
      <h2>Embedding your repository...</h2>
      <div className="progress-bar">
        <div className="progress" style={{ width: `${progress}%` }} />
      </div>
      <p>{progress}%</p>
    </div>
  );
};

export default LoaderPage;
