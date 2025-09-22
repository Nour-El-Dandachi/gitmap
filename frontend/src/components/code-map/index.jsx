import React, { useEffect, useCallback, useState } from "react";
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState,
} from "reactflow";
import "reactflow/dist/style.css";
import axios from "axios";
import dagre from "dagre";
import "./code-map.css";
import { toPng } from "html-to-image";
import { useRef } from "react";

const nodeWidth = 200;
const nodeHeight = 50;

const dagreGraph = new dagre.graphlib.Graph();
dagreGraph.setDefaultEdgeLabel(() => ({}));

function getLayoutedElements(nodes, edges, direction = "TB") {
  dagreGraph.setGraph({ rankdir: direction });
  nodes.forEach((node) =>
    dagreGraph.setNode(node.id, { width: nodeWidth, height: nodeHeight })
  );
  edges.forEach((edge) => dagreGraph.setEdge(edge.source, edge.target));
  dagre.layout(dagreGraph);

  return nodes.map((node) => {
    const pos = dagreGraph.node(node.id);
    return {
      ...node,
      position: { x: pos.x - nodeWidth / 2, y: pos.y - nodeHeight / 2 },
      targetPosition: "top",
      sourcePosition: "bottom",
    };
  });
}

function getNodeStyle(name) {
  if (name.endsWith("Controller.php"))
    return { backgroundColor: "#948BFC", color: "#fff", borderRadius: 10, padding: 10 };
  if (name.endsWith("Service.php"))
    return { backgroundColor: "#131325", color: "#fff", borderRadius: 10, padding: 10 };
  if (name.endsWith(".php") && !name.includes("Controller") && !name.includes("Service"))
    return { backgroundColor: "#D6D3F3", color: "#000", borderRadius: 10, padding: 10 };
  return { backgroundColor: "#D3D3D3", color: "#000", borderRadius: 10, padding: 10 };
}


const CodeMap = ({ repoId }) => {
  const reactFlowWrapper = useRef(null);

  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);

  const [chatOpen, setChatOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [currentQuestion, setCurrentQuestion] = useState("");
  const [activeFile, setActiveFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const token = localStorage.getItem("access");
  const [sessionId, setSessionId] = useState(null);


  const handleNodeClick = async (event, node) => {
    setActiveFile(node);
    setMessages([]);
    setChatOpen(true);

    try {
      const res = await axios.post(
        "http://localhost:8000/api/chat/sessions/",
        { repository_id: repoId },
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      );

      if (res.data.status === "success") {
        setSessionId(res.data.payload.session_id);
      } else {
        console.error("Failed to create chat session:", res.data);
      }
    } catch (err) {
      console.error("Error creating chat session:", err);
    }
  };


  const sendQuestion = async () => {
  if (!currentQuestion || !activeFile || !sessionId) return;

  const userMsg = { role: "user", text: currentQuestion };
  setMessages((prev) => [...prev, userMsg]);
  setCurrentQuestion("");
  setLoading(true);

  try {
    const res = await axios.post(
      "http://localhost:8000/api/chat/file/",
      {
        session_id: sessionId,
        file_id: parseInt(activeFile.id),
        question: userMsg.text,
      },
      {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      }
    );

    setMessages((prev) => [
      ...prev,
      { role: "ai", text: res.data.payload.answer || "[No answer]" },
    ]);
  } catch (err) {
    console.error("Chat failed:", err);
    setMessages((prev) => [
      ...prev,
      { role: "ai", text: "[Error getting answer]" },
    ]);
  } finally {
    setLoading(false);
  }
};


  const checkIfMapExists = async () => {
    try {
      const res = await axios.get(`http://localhost:8000/api/repos/${repoId}/exists/`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      return res.data.exists;
    } catch (err) {
      console.error("[Map Check] Failed:", err);
      return false;
    }
  };

  const fetchExistingMap = async () => {
    try {
      const res = await axios.get(`http://localhost:8000/api/map/data/${repoId}/`, {
        headers: { Authorization: `Bearer ${token}` },
      });

      const dbNodes = res.data.nodes.map((node) => ({
        id: String(node.file_id),
        data: { label: node.file_name },
        style: getNodeStyle(node.file_name),
        position: { x: node.x, y: node.y },
        targetPosition: "top",
        sourcePosition: "bottom",
      }));

      const dbEdges = res.data.edges.map((e) => ({
        id: `${e.source}-${e.target}`,
        source: String(e.source),
        target: String(e.target),
        animated: true,
        style: { stroke: "#131325" },
      }));

      setNodes(dbNodes);
      setEdges(dbEdges);
    } catch (err) {
      console.error("[Existing Map] Error loading map:", err);
    }
  };

  const fetchMapData = useCallback(async () => {
    const exists = await checkIfMapExists();
    if (exists) {
      await fetchExistingMap();
      return;
    }

    try {
      const res = await axios.get(
        `http://localhost:8000/api/repos/${repoId}/map-ai/`,
        { headers: { Authorization: `Bearer ${token}` } }
      );

      const markdown = res.data.markdown;
      const lines = markdown.split("\n").slice(2);
      const rawNodes = [];
      const rawEdges = [];

      lines.forEach((line) => {
        if (!line.includes("|")) return;
        const parts = line.split("|").map((p) => p.trim());
        if (parts.length < 4) return;

        const id = parts[1];
        const name = parts[2];
        const usedBy = parts[3];

        if (!id || !name) return;

        rawNodes.push({ id, file_name: name });

        if (usedBy) {
          usedBy.split(",").forEach((targetId) => {
            const target = targetId.trim();
            if (target) {
              rawEdges.push({ source: target, target: id });
            }
          });
        }
      });

      const layoutedNodes = getLayoutedElements(
        rawNodes.map((n) => ({
          id: n.id,
          data: { label: n.file_name },
          style: getNodeStyle(n.file_name),
          position: { x: 0, y: 0 },
        })),
        rawEdges.map((e) => ({ id: `${e.source}-${e.target}`, ...e }))
      );

      const finalNodes = layoutedNodes.map((n) => ({ ...n }));
      const finalEdges = rawEdges.map((e) => ({
        id: `${e.source}-${e.target}`,
        source: e.source,
        target: e.target,
        animated: true,
        style: { stroke: "#131325" },
      }));

      setNodes(finalNodes);
      setEdges(finalEdges);

      const nodesPayload = finalNodes.map((n) => ({
        repo_file: parseInt(n.id),
        x: n.position.x,
        y: n.position.y,
      }));

      const edgesPayload = rawEdges.map((e) => ({
        source: parseInt(e.source),
        target: parseInt(e.target),
      }));

      await axios.post("http://localhost:8000/api/map/nodes/", nodesPayload, {
        headers: { Authorization: `Bearer ${token}` },
      }).catch((err) => {
        console.error("[Save Nodes] Failed:", err.response?.data || err.message);
      });

      await axios.post("http://localhost:8000/api/map/edges/", edgesPayload, {
        headers: { Authorization: `Bearer ${token}` },
      }).catch((err) => {
        console.error("[Save Edges] Failed:", err.response?.data || err.message);
      });

      setTimeout(async () => {
        if (reactFlowWrapper.current) {
          try {
            const dataUrl = await toPng(reactFlowWrapper.current, {
              backgroundColor: "#ffffff",
            });
            localStorage.setItem(`repo-image-${repoId}`, dataUrl);
            const link = document.createElement("a");
            link.href = dataUrl;
            link.download = `repo-${repoId}.png`;
            link.click();
          } catch (err) {
            console.error("Failed to export map image:", err);
          }
        }
      }, 1000);

    } catch (err) {
      console.error("[Map-AI] Failed to generate map:", err);
    }
  }, [repoId, token]);


  useEffect(() => {
    const handleRunMetrics = async (e) => {
      const { repoId } = e.detail;
      

      try {
        await axios.post(
          `http://localhost:8000/api/metrics/extract/${repoId}/`,
          {},
          {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          }
        );

        
        await new Promise((resolve) => setTimeout(resolve, 3000));

        const predRes = await axios.post(
          `http://localhost:8000/api/metrics/predict/${repoId}/`,
          {},
          {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          }
        );

        await new Promise((resolve) => setTimeout(resolve, 2000));
        


        const results = predRes.data.results;

        setNodes((prevNodes) =>
          prevNodes.map((node) => {
            const pred = results.find((r) => String(r.repo_file_id) === node.id);
            if (!pred) return node;
            return {
              ...node,
              style: {
                ...node.style,
                border: `3px solid ${pred.pred === "true" ? "red" : "green"}`,
              },

            };
          })
        );
      } catch (err) {
        console.error("Metrics run failed:", err);
      }
    };

    window.addEventListener("runMetrics", handleRunMetrics);
    return () => window.removeEventListener("runMetrics", handleRunMetrics);
  }, [token, setNodes]);

  useEffect(() => {
    fetchMapData();
  }, [fetchMapData]);

  return (
    <div style={{ height: "90vh", width: "100%", display: "flex" }}>
      <div style={{ flex: 1 }} ref={reactFlowWrapper}>
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onNodeClick={handleNodeClick}
          fitView
        >
          <Background />
          <MiniMap nodeColor={(n) => n.style?.backgroundColor || "#ccc"} />
          <Controls />
        </ReactFlow>
      </div>

      {chatOpen && (
        <div className="chat-panel">
          <div className="chat-header">
            Chat about: {activeFile?.data?.label}
            <button className="close-btn" onClick={() => setChatOpen(false)}>
              ✕
            </button>
          </div>
          <div className="chat-messages">
            {messages.map((m, i) => (
              <div key={i} className={`message ${m.role}`}>
                {m.text}
              </div>
            ))}
            {loading && (
              <div className="message ai loader">
                <div className="loader-dot"></div>
                <div className="loader-dot"></div>
                <div className="loader-dot"></div>
              </div>
            )}
          </div>
          <div className="chat-input">
            <input
              value={currentQuestion}
              onChange={(e) => setCurrentQuestion(e.target.value)}
              placeholder="Ask about this file..."
              onKeyDown={(e) => e.key === "Enter" && sendQuestion()}
            />
            <button onClick={sendQuestion}>Send</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default CodeMap;
