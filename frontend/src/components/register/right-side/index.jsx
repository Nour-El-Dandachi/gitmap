import React, { useState } from "react";
import GithubButton from "../../shared/github-btn";
import Input from "../../shared/input";
import "./right-side.css";
import { useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { registerUser } from "../../../features/auth/authSlice";
import gitmapLogo from "../../../assets/logos/gitmap_2.png";

const RightSide = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [localError, setLocalError] = useState("");

  const { loading, error: reduxError } = useSelector((s) => s.auth);

  const handleRegister = () => {
    if (!name || !email || !password || !confirm) {
      setLocalError("All fields are required.");
      return;
    }
    if (password !== confirm) {
      setLocalError("Passwords do not match.");
      return;
    }

    dispatch(registerUser({ name, email, password }))
      .unwrap()
      .then(() => navigate("/dashboard"))
      .catch((err) => setLocalError(err));
  };

  return (
    <div className="register-left-side">
      <div className="register-logo">
        <img src={gitmapLogo} alt="GitMap logo" />
      </div>
      <div className="register-form">
        <h1>Welcome to gitmap!</h1>
        <GithubButton location={"register"} />
        <div className="divider">
          <span>OR</span>
        </div>

        <div className="register-inputs">
          <Input
            type="text"
            name="name"
            hint="Full Name"
            icon="user"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
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
          <Input
            type="password"
            name="confirm"
            hint="Confirm Password"
            icon="lock"
            value={confirm}
            onChange={(e) => setConfirm(e.target.value)}
          />
        </div>

        <button
          className="register-btn"
          disabled={loading}
          onClick={handleRegister}
        >
          {loading ? "Signing up..." : "Sign Up"}
        </button>
        <p className="under-btn-txt">
          Already have an account?{" "}
          <button
            className="register-link"
            onClick={() => navigate("/login")}
          >
            Log in
          </button>
        </p>
        {(localError || reduxError) && (
          <p className="form-error">{localError || reduxError}</p>
        )}
      </div>
    </div>
  );
};

export default RightSide;
