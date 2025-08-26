import React from "react";
import Input from "../../components/shared/input";
import './login.css';

const Login = () => {
    return (
        <div className="login-page">
            <Input hint={"email"} icon={"mail"}/>
            <Input hint={"password"} icon={"lock"}/>
        </div>
    );
}

export default Login;