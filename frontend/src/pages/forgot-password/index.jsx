import React from "react";
import Input from "../../components/shared/input";
import RightSide from "../../components/forgot-password/right-side";
import gitmapLogo from "../../assets/logos/gitmap_1.png";
import './forgot-password.css';

const ForgotPassword = () => {
    return (
    <div className="register-page">
      
      <div className="register-right-side">
        <div className="brand">
          <img src={gitmapLogo} alt="logo" className="big-logo" />
        </div>
      </div>
      <RightSide />
    </div>
  );
};


export default ForgotPassword;