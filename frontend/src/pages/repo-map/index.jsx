import CodeMap from "../../components/code-map/index.jsx"


const RepoMapPage = () => {

  const repoId = localStorage.getItem("selectedRepoId");
  return <CodeMap repoId={repoId} />;
}

export default RepoMapPage;
