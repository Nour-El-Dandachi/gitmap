import React from "react";
import './repository-box.css';
import RepoImg from "../../../assets/image.png"


const RepositoryBox = () => {
    return (
        <div className="repository-box">
            <div className="repo-img"><img className="repos-img" src={RepoImg}></img></div>
            <div className="repo-bottom">
            <div className="repo-title">Ecommerce-website</div>
            <div className="last-view">Viewed 5 minutes ago</div> 
            </div>
        </div>
    );
}

export default RepositoryBox;