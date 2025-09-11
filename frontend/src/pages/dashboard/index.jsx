import React, { useEffect, useState } from "react";
import './dashboard.css';
import SideBar from "../../components/shared/side-bar";
import Header from "../../components/shared/header";
import AddBox from "../../components/dashboard/add-box";
import RepositoryBox from "../../components/shared/repository-box";
import axios from "axios";
import { useSelector } from "react-redux";


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

const Dashboard = () => {
  const [repositories, setRepositories] = useState([]);
  const { access } = useSelector((s) => s.auth);

  useEffect(() => {
    const fetchRepos = async () => {
      try {
        const res = await axios.get("http://localhost:8000/api/repos/user/", {
          headers: { Authorization: `Bearer ${access}` },
        });

        if (res.data.status === "success") {
          setRepositories(res.data.payload);
        }
      } catch (err) {
        console.error("Failed to fetch repos", err);
      }
    };

    fetchRepos();
  }, [access]);

  return (
    <div className="dashboard-page">
      <SideBar />
      <div className="dashboard-right">
        <Header location={"Dashboard"} /> 
        <AddBox />
        <div className="box">
          <div className="recently-viewed-box">
            <h3>Recently Viewed</h3>
          </div>

          <div className="repositories">
            {repositories.length > 0 ? (
              repositories.map((repo) => (
                <RepositoryBox
                  key={repo.id}
                  name={repo.name}
                  createdAt={timeAgo(repo.created_at)}
                />
              ))
            ) : (
              <p>No repositories found.</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
