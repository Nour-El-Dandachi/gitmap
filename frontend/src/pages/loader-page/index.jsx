import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./loader-page.css";

const LoaderPage = () => {
  const navigate = useNavigate();
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    let current = 0;
    const interval = setInterval(() => {
      current += 10; // increase by 10%
      if (current >= 100) {
        clearInterval(interval);
        navigate("/map"); 
      }
      setProgress(current);
    }, 500); // every 0.5 seconds

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
