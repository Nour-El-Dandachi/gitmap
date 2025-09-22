import CodeMap from "../../components/code-map/index.jsx"
import { ChevronLeft } from 'lucide-react';
import { useNavigate } from "react-router-dom";
import "./repo-map.css"


const RepoMapPage = () => {
  const navigate = useNavigate();
  const repoId = localStorage.getItem("selectedRepoId");
  const repoName = localStorage.getItem("selectedRepoName");
  return (
    <div>
    <div className="map-header">
      <div className="location" onClick={() => navigate("/dashboard")}>
        <ChevronLeft />
        <h1>{repoName}</h1>
      </div>

      <div className="right-header-map">
        <div className="legend">
          <div className="stable">
            <div className="green-dot"></div>
            Stable

          </div>
          <div className="unstable">
            <div className="red-dot"></div>
            Unstable
          </div>
        </div>
        <button 
                className="metrics-btn" 
                onClick={() => window.dispatchEvent(new CustomEvent("runMetrics", { detail: { repoId } }))}
              >
                Run Metrics
        </button>
      </div>

      
    </div>

    
    <CodeMap repoId={repoId} />

    </div>


  );
};

export default RepoMapPage;
