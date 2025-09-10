import React from "react";
import './notifications.css';
import SideBar from "../../components/shared/side-bar";
import Header from "../../components/shared/header";
import NotificationCard from "../../components/notification-card";

const Notifications= () => {
    return (
    <div className="notifications-page">=
      <SideBar name={"Nour El Dandachi"} />
      <div className="dashboard-right">
        <Header location={"Notifications"} />

      </div>
    </div>
  );
};


export default Notifications;