import React from "react";
import Input from "../../shared/input";
import "./right-side.css";
import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import gitmapLogo from "../../../assets/logos/gitmap_2.png";


const RightSide = () => {
    const navigate = useNavigate();

  const [password, setPassword] = useState();
  const [error, setError] = useState("");

  return (
    <div className="register-left-side">
      <div className="register-logo"><img src={gitmapLogo}></img></div>
      <div className="register-form">
        <h1>Reset Password</h1>

        <div className="register-inputs">
          <Input hint={"Password"} icon={"lock"} />
          <Input hint={"Confirm Password"} icon={"lock"} />
          
        </div>

        <button className="register-btn">Reset Password</button>
        
          {error && <p className="form-error">{error}</p>}
        
      </div>
    </div>
  );
};

export default RightSide;
