import React from 'react';
import Login from '../pages/login/index.jsx'
import Register from '../pages/register/index.jsx'
import Home from '../pages/home/index.jsx';
import {Routes,Route} from 'react-router-dom';
import ForgotPassword from '../pages/forgot-password/index.jsx';
import ResetPassword from '../pages/reset-password/index.jsx';
import Dashboard from '../pages/dashboard/index.jsx';



const MyRoutes = ()=>{

    return (
        <Routes>
            <Route path='/login' element={<Login />}/>
            <Route path='/register' element={<Register />}/>
            <Route path='/forgot-password' element={<ForgotPassword />}/>
            <Route path='/reset-password' element={<ResetPassword />}/>
            <Route path='/dashboard' element={<Dashboard />}/>
            <Route path='/home' element={<Home />}/>
        </Routes>
    );
}

export default MyRoutes;