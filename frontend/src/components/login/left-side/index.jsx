import React, { useState } from "react";
import GithubButton from "../../shared/github-btn";
import Input from "../../shared/input";
import "./left-side.css";
import { useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { loginUser } from "../../../features/auth/authSlice";
import gitmapLogo from "../../../assets/logos/gitmap_2.png";

const LeftSide = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [localError, setLocalError] = useState("");

  const { loading, error: reduxError } = useSelector((s) => s.auth);

  const handleLogin = () => {
    if (!email || !password) {
      setLocalError("Please enter both email and password.");
      return;
    }
    dispatch(loginUser({ email, password }))
      .unwrap()
      .then(() => navigate("/dashboard"))
      .catch((err) => setLocalError(err));
  };

  return (
    <div className="login-left-side">
      <div className="login-logo">
        <img src={gitmapLogo} alt="GitMap logo" />
      </div>
      <div className="login-form">
        <h1>Welcome back to gitmap!</h1>
        <GithubButton location={"login"} />
        <div className="divider">
          <span>OR</span>
        </div>

        <div className="login-inputs">
          <Input
            type="email"
            name="email"
            hint="Email"
            icon="mail"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <Input
            type="password"
            name="password"
            hint="Password"
            icon="lock"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>

        <button className="login-btn" disabled={loading} onClick={handleLogin}>
          {loading ? "Logging in..." : "Log in"}
        </button>
        <p className="under-btn-txt">
          Don't have an account?{" "}
          <button
            className="signup-link"
            onClick={() => navigate("/register")}
          >
            Sign up
          </button>
        </p>
        {(localError || reduxError) && (
          <p className="form-error">{localError || reduxError}</p>
        )}

      </div>
    </div>
  );
};

export default LeftSide;
