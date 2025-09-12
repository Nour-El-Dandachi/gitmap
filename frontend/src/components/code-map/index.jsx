import React, { useEffect, useState, useCallback } from "react";
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState,
  addEdge,
} from "reactflow";
import "reactflow/dist/style.css";
import axios from "axios";

const CodeMap = ({ repoId }) => {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);

  const fetchMapData = useCallback(async () => {
    try {
      const token = localStorage.getItem("access");
      const res = await axios.get( 
        `http://localhost:8000/api/repos/${repoId}/map-ai/`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      console.log(res.data);

      
      const fetchedNodes = res.data.nodes.map((node, index) => ({
        id: node.id,
        data: { label: node.label },
        position: { x: (index % 5) * 250, y: Math.floor(index / 5) * 150 },
      }));

      const fetchedEdges = res.data.edges.map((edge) => ({
        id: `${edge.source}-${edge.target}`,
        source: edge.source,
        target: edge.target,
        animated: true,
      }));

      setNodes(fetchedNodes);
      setEdges(fetchedEdges);
    } catch (error) {
      console.error("Failed to fetch map data", error);
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
        <MiniMap />
        <Controls />
      </ReactFlow>
    </div>
  );
};

export default CodeMap;
