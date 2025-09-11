import React, { useState } from "react";
import './add-box.css';
import { SendHorizontal } from "lucide-react";
import axios from "axios";
import { useSelector } from "react-redux";

const AddBox = () => {
  const [url, setUrl] = useState("");
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(false);

  const { access } = useSelector((s) => s.auth);

  const handleAddRepo = async () => {
    if (!url) {
      setStatus("Please enter a repository URL.");
      return;
    }
    try {
      setLoading(true);
      setStatus(null);

      const res = await axios.post(
        "http://localhost:8000/api/repos/add/",
        { url },
        { headers: { Authorization: `Bearer ${access}` } }
      );

      if (res.data.status === "success") {
        setStatus(`${res.data.payload.repo_name} added!`);
        setUrl("");
      } else {
        setStatus("Something went wrong.");
      }
    } catch (err) {
      console.error(err);
      setStatus("Failed to add repository.");
    } finally {
      setLoading(false);
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
        {loading ? "..." : <SendHorizontal />}
      </div>
      {status && <p className="status-msg">{status}</p>}
    </div>
  );
};

export default AddBox;
