import React, { useEffect, useState } from "react";
import "./my-repositories.css";
import SideBar from "../../components/shared/side-bar";
import Header from "../../components/shared/header";
import RepositoryBox from "../../components/shared/repository-box";
import { Search } from "lucide-react";
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

const MyRepositories = () => {
  const [repositories, setRepositories] = useState([]);
  const [search, setSearch] = useState("");
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
        console.error("Failed to fetch repositories", err);
      }
    };

    fetchRepos();
  }, [access]);

  const filteredRepos = repositories.filter((repo) =>
    repo.name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="dashboard-page">
      <SideBar />
      <div className="dashboard-right">
        <Header location={"My Repositories"} />
        
        <div className="repo-search">
          <Search />
          <input
            className="search-input"
            placeholder="Search for anything"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>

        <div className="repositories">
          {filteredRepos.length > 0 ? (
            filteredRepos.map((repo) => (
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
  );
};

export default MyRepositories;
