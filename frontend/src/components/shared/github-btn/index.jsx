import React from "react";
import "./github-btn.css";
import githubLogo from "../../../assets/logos/github-logo.png";

const GithubButton = ({ location }) => {
  return (
    <div className="github-btn-wrapper">
      <div className="github-img">
        <img src={githubLogo} alt="GitHub Logo" />
      </div>
      <div className="github-btn-text">
        {location === "login" ? "Continue with GitHub" : "Sign up with GitHub"}
      </div>
    </div>
  );
};

export default GithubButton;
