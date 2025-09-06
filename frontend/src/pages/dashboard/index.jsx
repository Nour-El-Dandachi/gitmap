import React from "react";
import './dashboard.css';
import SideBar from "../../components/shared/side-bar";
import Header from "../../components/shared/header";
import AddBox from "../../components/dashboard/add-box";
import RepositoryBox from "../../components/shared/repository-box";

const Dashboard = () => {
    return (
        <div className="dashboard-page">
            <SideBar name={"Nour El Dandachi"}/>
            <div className="dashboard-right">
               <Header location={"Dashboard"} /> 
               <AddBox />
               <div className="box">
               <div className="recently-viewed-box">
                
                <h3>Recently Viewed</h3>

               </div>

               <div className="repositories">
                    <RepositoryBox />
                    <RepositoryBox />
                    <RepositoryBox />
                    <RepositoryBox />
                    <RepositoryBox />
                    <RepositoryBox />
                    <RepositoryBox />
                    <RepositoryBox />
                    <RepositoryBox />
                    <RepositoryBox />
                    <RepositoryBox />
                    <RepositoryBox />
                    <RepositoryBox />
                    <RepositoryBox />
                    <RepositoryBox />
                    <RepositoryBox />
               </div>
               </div>
            </div>
            
        </div>
    );
}

export default Dashboard;