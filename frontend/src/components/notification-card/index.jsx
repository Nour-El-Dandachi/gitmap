import React from "react";
import './notification-card.css';
import { CheckCheck } from 'lucide-react';

function timeAgo(dateString) {
  const date = new Date(dateString);
  const now = new Date();
  const diffMs = now - date;

  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMins / 60);
  const diffDays = Math.floor(diffHours / 24);

  if (diffMins < 1) return "Just now";
  if (diffMins < 60) return `${diffMins} minute${diffMins > 1 ? "s" : ""} ago`;
  if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? "s" : ""} ago`;
  return `${diffDays} day${diffDays > 1 ? "s" : ""} ago`;
}

const NotificationCard = ({ message, is_read, created_at }) => {
  return (
    <div className={`notification-card ${is_read ? "read" : "unread"}`}>
      <div className="notif-header">
        <div className="head-left">
          <div className={`circle-read ${is_read ? "read" : ""}`}></div>
          <div className="notification-text">{message}</div>
        </div>
        <div className="head-right">{timeAgo(created_at)}</div>
      </div>
      <div className="notif-bottom">
        <div className="mark-as-read"><CheckCheck size={18}/> Mark as read</div>
        <div className="delete-btn">Delete</div>
      </div>
    </div>
  );
};

export default NotificationCard;
