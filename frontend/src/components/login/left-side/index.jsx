import React from "react";
import GithubButton from "../../shared/github-btn";
import './left-side.css';


const LeftSide = () => {
    return (
        <div className="login-left-side">
            <div className="login-logo">
                
            </div>
            <div className="login-form">
                <h1>Welome back to gitmap!</h1>
                <GithubButton location={"login"} />
            </div>
        </div>
    );
}

export default LeftSide;