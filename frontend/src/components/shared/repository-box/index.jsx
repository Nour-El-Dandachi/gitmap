import React from "react";
import './repository-box.css';
import RepoImg from "../../../assets/image.png";

const RepositoryBox = ({ name, createdAt }) => {
  return (
    <div className="repository-box">
      <div className="repo-img">
        <img className="repos-img" src={RepoImg} alt="repo" />
      </div>
      <div className="repo-bottom">
        <div className="repo-title">{name}</div>
        <div className="last-view">{createdAt}</div>
      </div>
    </div>
  );
};

export default RepositoryBox;
