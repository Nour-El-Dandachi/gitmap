import React from "react";
import "./github-btn.css";

const GithubButton = ({ location }) => {
  return (
    <div className="github-btn-wrapper">
      <div className="github-img"></div>
      <div className="github-btn-text">
        {location === "login" ? "Continue with GitHub" : "Sign up with GitHub"}
      </div>
    </div>
  );
};

export default GithubButton;