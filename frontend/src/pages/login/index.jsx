import React from "react";
import Input from "../../components/shared/input";
import './login.css';

const Login = () => {
    return (
        <div>
            <Input hint={"email"} icon={"mail"}/>
        </div>
    );
}

export default Login;