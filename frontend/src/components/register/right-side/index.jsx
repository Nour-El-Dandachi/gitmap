import React from "react";
import GithubButton from "../../shared/github-btn";
import Input from "../../shared/input";
import "./right-side.css";
import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import gitmapLogo from "../../../assets/logos/gitmap_2.png";


const RightSide = () => {
    const navigate = useNavigate();

  const [email, setEmail] = useState();
  const [password, setPassword] = useState();
  const [error, setError] = useState("");

  return (
    <div className="register-left-side">
      <div className="register-logo"><img src={gitmapLogo}></img></div>
      <div className="register-form">
        <h1>Welcome to gitmap!</h1>
        <GithubButton location={"register"} />
        <div className="divider">
          <span>OR</span>
        </div>

        <div className="register-inputs">
            <Input hint={"Full Name"} icon={"user"} />
          <Input hint={"Email"} icon={"mail"} />
          <Input hint={"Password"} icon={"lock"} />
          <Input hint={"Confirm Password"} icon={"lock"} />
        </div>

        <button className="register-btn">Sign Up</button>
        <p className="under-btn-txt">
          Already have an account?{" "}
          <button
            className="register-link"
            onClick={() => {
              navigate("/login");
            }}
          >
            Log in
          </button>
          {error && <p className="form-error">{error}</p>}
        </p>
      </div>
    </div>
  );
};

export default RightSide;
