import React from 'react';
import Login from '../pages/login/index.jsx'
import Register from '../pages/register/index.jsx'
import {Routes,Route} from 'react-router-dom';


const MyRoutes = ()=>{

    return (
        <Routes>
            <Route path='/login' element={<Login />}/>
            <Route path='/register' element={<Register />}/>
        </Routes>
    );
}
