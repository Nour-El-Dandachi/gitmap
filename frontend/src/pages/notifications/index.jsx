import React from "react";
import './notifications.css';
import SideBar from "../../components/shared/side-bar";
import Header from "../../components/shared/header";
import { Search } from "lucide-react";
import NotificationCard from "../../components/notification-card";

const Notifications= () => {
    return (
    <div className="notifications-page">
      <SideBar name={"Nour El Dandachi"} />
      <div className="notifications-right">
        <Header location={"Notifications"} />
        <div className="repo-search">
          <Search />{" "}
          <input className="search-input" placeholder="Search for anything" />
        </div>

        <NotificationCard message={"this is a test notification"}/>
        <NotificationCard message={"this is a test notification"} />
      </div>
      
    </div>
  );
};


export default Notifications;