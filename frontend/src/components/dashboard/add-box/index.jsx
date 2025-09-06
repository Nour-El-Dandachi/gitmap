import React from "react";
import './add-box.css';
import { SendHorizontal } from "lucide-react";

const AddBox = () => {
    return (
        <div className="add-box">
            <div className="url-box">Add Repository URL</div>
            <div className="send-icon"><SendHorizontal /></div>
        </div>
    );
}

export default AddBox;