import React from "react";
import "./side-bar.css";
import { Bell, Github, LayoutDashboard, Search, ChevronDown, UserRound, LogOut} from "lucide-react";
import gitmapLogo from "../../../assets/logos/gitmap_3.png";
import { useSelector } from "react-redux";

import { useNavigate, useLocation } from "react-router-dom";

const SideBar = () => {
  const { user } = useSelector((s) => s.auth);
  const navigate = useNavigate();
  const location = useLocation();

  const isActive = (path) => location.pathname === path;

  return (
    <div className="side-bar">
      <div className="header-img">
        <img src={gitmapLogo} alt="logo" className="logo" />
      </div>
      <div className="bar-profile">
        <div className="profile-photo"><UserRound /></div>
        <div className="profile-name">{user?.name}</div>
      </div>

      <div className="bar-menu">
        <div
          className={`menu-item ${isActive("/dashboard") ? "active" : ""}`}
          onClick={() => navigate("/dashboard")}
        >
          <LayoutDashboard /> Dashboard
        </div>
        <div
          className={`menu-item ${isActive("/my-repositories") ? "active" : ""}`}
          onClick={() => navigate("/my-repositories")}
        >
          <Github /> My Repositories
        </div>
        <div
          className={`menu-item ${isActive("/notifications") ? "active" : ""}`}
          onClick={() => navigate("/notifications")}
        >
          <Bell /> Notifications
        </div>
        <div
          className={`menu-item ${isActive("/login") ? "active" : ""}`}
          onClick={() => navigate("/login")}
        >
          <LogOut /> Log out
        </div>
      </div>
    </div>
  );
};


export default SideBar;
