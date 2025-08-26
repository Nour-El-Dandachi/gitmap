import React from "react";
import './input.css';

const Input = ({ type, name, hint, onChange, value }) => {
  return (
    <div className="input-wrapper">
      <input type={type} name={name} placeholder={hint} onChange={onChange} value={value}/>
    </div>
  );
}

export default Input;