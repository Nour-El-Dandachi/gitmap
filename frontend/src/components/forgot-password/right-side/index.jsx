import React from "react";
import Input from "../../shared/input";
import "./right-side.css";
import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import gitmapLogo from "../../../assets/logos/gitmap_2.png";


const RightSide = () => {
    const navigate = useNavigate();

  const [email, setEmail] = useState();
  const [error, setError] = useState("");

  return (
    <div className="register-left-side">
      <div className="register-logo"><img src={gitmapLogo}></img></div>
      <div className="register-form">
        <h1>Forgot Password?</h1>
        <p>Don’t worry we’ll send you reset instructions.</p>

        <div className="register-inputs">
          <Input hint={"Email"} icon={"mail"} />
          
        </div>

        <button className="register-btn">Send Email</button>
        <p className="under-btn-txt">
          Back to{" "}
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
