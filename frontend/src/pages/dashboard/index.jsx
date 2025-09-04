import React from "react";
import './dashboard.css';
import SideBar from "../../components/shared/side-bar";
import Header from "../../components/shared/header";

const Dashboard = () => {
    return (
        <div className="dashboard-page">
            <SideBar name={"Nour El Dandachi"}/>
            <Header location={"Dashboard"} />
        </div>
    );
}

export default Dashboard;