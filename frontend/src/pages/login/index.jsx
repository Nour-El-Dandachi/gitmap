import React from "react";
import Input from "../../components/shared/input";
import LeftSide from "../../components/login/left-side";
import gitmapLogo from "../../assets/logos/gitmap_1.png";
import './login.css';

const Login = () => {
    return (
    <div className="login-page">
      <LeftSide />
      <div className="login-right-side">
        <div className="brand">
          <img src={gitmapLogo} alt="logo" className="big-logo" />
        </div>
      </div>
    </div>
  );
};


export default Login;