import React from "react";
import './repository-box.css';
import RepoImg from "../../../assets/image.png";
import { useNavigate } from "react-router-dom";

const RepositoryBox = ({ id, name, createdAt }) => {
  const navigate = useNavigate();
  const savedImage = localStorage.getItem(`repo-image-${id}`);

  const handleClick = () => {
    localStorage.setItem("selectedRepoId", id);
    localStorage.setItem("selectedRepoName", name);
    navigate("/map");
  };

  return (
    <div className="repository-box" onClick={handleClick} style={{ cursor: "pointer" }}>
      <div className="repo-img">
        <img
          className="repos-img"
          src={savedImage || RepoImg}
          alt="repo"
        />
      </div>
      <div className="repo-bottom">
        <div className="repo-title">{name}</div>
        <div className="last-view">{createdAt}</div>
      </div>
    </div>
  );
};


export default RepositoryBox;

