import React from "react";
import "./my-repositories.css"
import SideBar from "../../components/shared/side-bar";
import Header from "../../components/shared/header";
import RepositoryBox from "../../components/shared/repository-box";
import { Search } from "lucide-react";

const MyRepositories = () => {
  return (
    <div className="dashboard-page">
      <SideBar/>
      <div className="dashboard-right">
        <Header location={"My Repositories"} />
        <div className="repo-search">
          <Search />{" "}
          <input className="search-input" placeholder="Search for anything" />
          
        </div>
        <div className="repositories">
                    <RepositoryBox />
                    <RepositoryBox />
                    <RepositoryBox />
                    <RepositoryBox />
                    <RepositoryBox />
                    <RepositoryBox />
                    <RepositoryBox />
                    <RepositoryBox />
                    <RepositoryBox />
                    <RepositoryBox />
                    <RepositoryBox />
                    <RepositoryBox />
                    <RepositoryBox />
                    <RepositoryBox />
                    <RepositoryBox />
                    <RepositoryBox />
               </div>
      </div>
    </div>
  );
};

export default MyRepositories;
