import React from "react";
import './notification-card.css';
import { CheckCheck } from 'lucide-react';

const NotificationCard = ({message, is_read, created_at}) => {
    return (
    <div className="notification-card">
        <div className="notif-header">
            <div className="head-left">
                <div className="circle-read"></div>
                <div className="notification-text">{message}</div>
            </div> 
            <div className="head-right">34 minutes ago</div>
        </div>
        <div className="notif-bottom">
        <div className="mark-as-read"><CheckCheck size={18}/> Mark as read</div>
        <div className="delete-btn">Delete</div>
        </div>
     

    </div>
  );
};


export default NotificationCard;