import React, { useEffect, useCallback } from "react";
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

const nodeWidth = 200;
const nodeHeight = 50;

const dagreGraph = new dagre.graphlib.Graph();
dagreGraph.setDefaultEdgeLabel(() => ({}));

function getLayoutedElements(nodes, edges, direction = "TB") {
  dagreGraph.setGraph({ rankdir: direction });

  nodes.forEach((node) => {
    dagreGraph.setNode(node.id, { width: nodeWidth, height: nodeHeight });
  });

  edges.forEach((edge) => {
    dagreGraph.setEdge(edge.source, edge.target);
  });

  dagre.layout(dagreGraph);

  return nodes.map((node) => {
    const nodeWithPosition = dagreGraph.node(node.id);
    node.targetPosition = "top";
    node.sourcePosition = "bottom";
    return {
      ...node,
      position: {
        x: nodeWithPosition.x - nodeWidth / 2,
        y: nodeWithPosition.y - nodeHeight / 2,
      },
    };
  });
}

function getNodeStyle(name) {
  if (name.endsWith("Controller.php")) {
    return { backgroundColor: "#948BFC", color: "#fff", borderRadius: 10, padding: 10 };
  }
  if (name.endsWith("Service.php")) {
    return { backgroundColor: "#131325", color: "#fff", borderRadius: 10, padding: 10 };
  }
  if (name.endsWith(".php") && !name.includes("Controller") && !name.includes("Service")) {
    return { backgroundColor: "#D6D3F3", color: "#000", borderRadius: 10, padding: 10 };
  }
  return { backgroundColor: "#D3D3D3", color: "#000", borderRadius: 10, padding: 10 };
}

const CodeMap = ({ repoId }) => {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const token = localStorage.getItem("access");

  const checkIfMapExists = async () => {
    try {
      const res = await axios.get(`http://localhost:8000/api/repos/${repoId}/exists/`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      console.log("[Map Check] Map exists?", res.data.exists);
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

      console.log("[Existing Map] Loaded nodes & edges:", dbNodes, dbEdges);
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

      console.log("[New Map] Parsed nodes:", finalNodes);
      console.log("[New Map] Parsed edges:", finalEdges);

      setNodes(finalNodes);
      setEdges(finalEdges);

      console.log(finalNodes)
      console.log(finalEdges)

      const nodesPayload = finalNodes.map((n) => ({
        repo_file: parseInt(n.id),
        x: n.position.x,
        y: n.position.y,
      }));

      const edgesPayload = rawEdges.map((e) => ({
        source: parseInt(e.source),
        target: parseInt(e.target),
      }));

      console.log("[Save] Posting node positions:", nodesPayload);
      await axios.post("http://localhost:8000/api/map/nodes/", nodesPayload, {
        headers: { Authorization: `Bearer ${token}` },
      }).catch((err) => {
        console.error("[Save Nodes] Failed:", err.response?.data || err.message);
      });

      console.log("[Save] Posting edges:", edgesPayload);
      await axios.post("http://localhost:8000/api/map/edges/", edgesPayload, {
        headers: { Authorization: `Bearer ${token}` },
      }).catch((err) => {
        console.error("[Save Edges] Failed:", err.response?.data || err.message);
      });

    } catch (err) {
      console.error("[Map-AI] Failed to generate map:", err);
    }
  }, [repoId]);

  useEffect(() => {
    fetchMapData();
  }, [fetchMapData]);

  return (
    <div style={{ height: "100vh", width: "100%" }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        fitView
      >
        <Background />
        <MiniMap nodeColor={(n) => n.style?.backgroundColor || "#ccc"} />
        <Controls />
      </ReactFlow>
    </div>
  );
};

export default CodeMap;
