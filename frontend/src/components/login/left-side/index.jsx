import React from "react";
import GithubButton from "../../shared/github-btn";
import Input from "../../shared/input";
import "./left-side.css";
import { icons } from "lucide-react";

const LeftSide = () => {
  return (
    <div className="login-left-side">
      <div className="login-logo"></div>
      <div className="login-form">
        <h1>Welome back to gitmap!</h1>
        <GithubButton location={"login"} />
        <div className="divider">
          <span>OR</span>
        </div>

        <div className="login-inputs">
          <Input hint={"Email"} icon={"mail"} />
          <Input hint={"Password"} icon={"lock"} />
        </div>
      </div>
    </div>
  );
};

export default LeftSide;
