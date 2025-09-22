import React from "react";
import "./github-btn.css";
import githubLogo from "../../../assets/logos/github-logo.png";

const GithubButton = ({ location }) => {
  const handleClick = () => {
    window.location.href = "http://localhost:8000/auth/github/redirect";
  };

  return (
    <button type="button" className="github-btn-wrapper" onClick={handleClick}>
      <div>
        <img className="github-img" src={githubLogo} alt="GitHub Logo" />
      </div>
      <div className="github-btn-text">
        {location === "login" ? "Continue with GitHub" : "Sign up with GitHub"}
      </div>
    </button>
  );
};

export default GithubButton;
