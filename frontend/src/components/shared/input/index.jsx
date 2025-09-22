import React from "react";
import { Mail, Lock, UserRound } from "lucide-react";
import "./input.css";

const Input = ({ type, name, hint, onChange, icon, value }) => {
  const setIcon = () => {
    if (icon === "lock") {
      return <Lock className="icon" color="#131325" />;
    } else if (icon === "mail") {
      return <Mail className="icon" color="#131325" />;
    }
    else{
      return <UserRound className="icon" color="#131325" />;
    }
  };
  return (
    <div className="input-wrapper">
      {setIcon()}
      <input
        type={type}
        name={name}
        placeholder={hint}
        onChange={onChange}
        value={value}
      />
    </div>
  );
};

export default Input;
