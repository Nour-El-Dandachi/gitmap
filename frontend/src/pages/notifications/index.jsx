import React, { useEffect, useState } from "react";
import './notifications.css';
import SideBar from "../../components/shared/side-bar";
import Header from "../../components/shared/header";
import { Search } from "lucide-react";
import NotificationCard from "../../components/notification-card";
import axios from "axios";
import { useSelector } from "react-redux";

const Notifications = () => {
  const [notifications, setNotifications] = useState([]);
  const [search, setSearch] = useState("");
  const { access } = useSelector((s) => s.auth);

  useEffect(() => {
    const fetchNotifications = async () => {
      try {
        const res = await axios.get("http://localhost:8000/api/notifications/", {
          headers: { Authorization: `Bearer ${access}` },
        });
        if (res.data.status === "success") {
          setNotifications(res.data.payload);
        }
      } catch (err) {
        console.error("Failed to fetch notifications", err);
      }
    };

    fetchNotifications();
  }, [access]);

  const handleMarkRead = async (id) => {
    try {
      const res = await axios.post(
        `http://localhost:8000/api/notifications/${id}/mark-read/`,
        {},
        { headers: { Authorization: `Bearer ${access}` } }
      );

      if (res.data.status === "success") {
        setNotifications((prev) =>
          prev.map((n) =>
            n.id === id ? { ...n, is_read: true } : n
          )
        );
      }
    } catch (err) {
      console.error("Failed to mark as read", err);
    }
  };

  const filtered = notifications.filter((n) =>
    n.message.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="notifications-page">
      <SideBar/>
      <div className="notifications-right">
        <Header location={"Notifications"} />

        <div className="repo-search">
          <Search />
          <input
            className="search-input"
            placeholder="Search for anything"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>

        {filtered.length > 0 ? (
          filtered.map((n) => (
            <NotificationCard
              key={n.id}
              id={n.id}
              message={n.message}
              is_read={n.is_read}
              created_at={n.created_at}
              onMarkRead={handleMarkRead}
            />
          ))
        ) : (
          <p>No notifications found.</p>
        )}
      </div>
    </div>
  );
};


export default Notifications;
