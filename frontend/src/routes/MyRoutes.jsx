import React from 'react';
import Login from '../pages/login/index.jsx'
import {Routes,Route} from 'react-router-dom';


const MyRoutes = ()=>{

    return (
        <Routes>
            <Route path='/login' element={<Login />}/>
        </Routes>
    );
}
