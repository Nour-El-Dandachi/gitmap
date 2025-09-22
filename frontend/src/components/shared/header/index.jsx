import React from "react";
import "./header.css";

const Header = ({location}) => {
  return (
    <div className="header">
      <div className="location">
        <h1>{location}</h1>
      </div>
    </div>
  );
};

export default Header;
