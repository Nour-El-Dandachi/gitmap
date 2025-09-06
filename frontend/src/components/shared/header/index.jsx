import React from "react";
import "./header.css";
import gitmapLogo from "../../../assets/logos/gitmap_3.png";

const Header = ({location}) => {
  return (
    <div className="header">
      <div className="location">
        <h1>{location}</h1>
      </div>
      <div className="header-img">
        <img src={gitmapLogo} alt="logo" className="logo" />
      </div>
      
    </div>
  );
};

export default Header;
