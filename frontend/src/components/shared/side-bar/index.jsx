import React from "react";
import "./side-bar.css";
import { Bell, Github, LayoutDashboard, Search, ChevronDown, UserRound } from "lucide-react";
import gitmapLogo from "../../../assets/logos/gitmap_3.png";

const SideBar = ({name}) => {
  return (
    <div className="side-bar">
      <div className="header-img">
        <img src={gitmapLogo} alt="logo" className="logo" />
      </div>
      <div className="bar-profile">
        <div className="profile-photo"><UserRound /></div>
        <div className="profile-name"> {name} <ChevronDown /></div>
      </div>
      {/* <div className="bar-search">
        <Search /> <input className="search-input" placeholder="Search for anything" />
      </div> */}
      <div className="bar-menu">
            <div className="menu-dashboard"><LayoutDashboard/> Dashboard</div>
            <div className="menu-repositories"><Github/> My Repositories</div>
            <div className="menu-notifications"><Bell/> Notifications</div>
      </div>
      
    </div>
  );
};

export default SideBar;
