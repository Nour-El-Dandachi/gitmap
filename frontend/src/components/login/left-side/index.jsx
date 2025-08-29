import React from "react";
import GithubButton from "../../shared/github-btn";
import Input from "../../shared/input";
import "./left-side.css";
import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import gitmapLogo from "../../../assets/logos/gitmap_2.png";


const LeftSide = () => {
    const navigate = useNavigate();

  const [email, setEmail] = useState();
  const [password, setPassword] = useState();
  const [error, setError] = useState("");

  return (
    <div className="login-left-side">
      <div className="login-logo"><img src={gitmapLogo}></img></div>
      <div className="login-form">
        <h1>Welcome back to gitmap!</h1>
        <GithubButton location={"login"} />
        <div className="divider">
          <span>OR</span>
        </div>

        <div className="login-inputs">
          <Input hint={"Email"} icon={"mail"} />
          <Input hint={"Password"} icon={"lock"} />
        </div>

        <button className="login-btn">Log in</button>
        <p className="under-btn-txt">
          Don't have an account?{" "}
          <button
            className="signup-link"
            onClick={() => {
              navigate("/register");
            }}
          >
            Sign up
          </button>
          {error && <p className="form-error">{error}</p>}
        </p>
      </div>
    </div>
  );
};

export default LeftSide;
