import React from "react";
import "./side-bar.css";
import { Bell, Github, LayoutDashboard, Search, ChevronDown, UserRound } from "lucide-react";

const SideBar = ({name}) => {
  return (
    <div className="side-bar">
      <div className="bar-profile">
        <div className="profile-photo"><UserRound /></div>
        <div className="profile-name"> {name} <ChevronDown /></div>
      </div>
      <div className="bar-search">
        <Search /> <input className="search-input" placeholder="Search for anything" />
      </div>
      <div className="bar-menu">
            <div className="menu-dashboard"><LayoutDashboard/> Dashboard</div>
            <div className="menu-repositories"><Github/> My Repositories</div>
            <div className="menu-notifications"><Bell/> Notifications</div>
      </div>
      
    </div>
  );
};

export default SideBar;
