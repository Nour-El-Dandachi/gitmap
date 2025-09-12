import React, { useState } from "react";
import './add-box.css';
import { SendHorizontal } from "lucide-react";
import axios from "axios";
import { useSelector } from "react-redux";
import LoaderPage from "../../../pages/loader-page";
import { useNavigate } from "react-router-dom";

const AddBox = () => {
  const [url, setUrl] = useState("");
  const [status, setStatus] = useState(null);
  const { access } = useSelector((s) => s.auth);
  const navigate = useNavigate();

  const handleAddRepo = async () => {
    if (!url) {
      setStatus("Please enter a repository URL.");
      return;
    }
    try {
      setStatus(null);
      // Call backend
      await axios.post(
        "http://localhost:8000/api/repos/add/",
        { url },
        { headers: { Authorization: `Bearer ${access}` } }
      );

      // Instantly redirect to fake loader page
      navigate("/loader");
    } catch (err) {
      console.error(err);
      setStatus("Failed to add repository.");
    }
  };

  return (
    <div className="add-box">
      <input
        type="text"
        placeholder="Add Repository URL"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        className="url-box"
      />
      <div className="send-icon" onClick={handleAddRepo}>
        <SendHorizontal />
      </div>
      {status && <p className="status-msg">{status}</p>}
    </div>
  );
};

export default AddBox;
