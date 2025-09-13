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

      const markdown = res.data.markdown;
      const lines = markdown.split("\n").slice(2); // remove header

      const nodeSet = new Set();
      const edgeList = [];

      lines.forEach((line) => {
        const parts = line.split("|").map((part) => part.trim());
        if (parts.length < 3) return;
        const file = parts[1];
        const usedByRaw = parts[2];
        nodeSet.add(file);

        if (usedByRaw) {
          usedByRaw.split(",").forEach((consumer) => {
            const target = consumer.trim();
            if (target) {
              nodeSet.add(target);
              edgeList.push({ source: target, target: file });
            }
          });
        }
      });

      const rawNodes = Array.from(nodeSet).map((name) => ({
        id: name,
        data: { label: name },
        position: { x: 0, y: 0 },
      }));

      const rawEdges = edgeList.map((e) => ({
        id: `${e.source}-${e.target}`,
        source: e.source,
        target: e.target,
        animated: true,
      }));

      const layoutedNodes = getLayoutedElements(rawNodes, rawEdges);

      setNodes(layoutedNodes);
      setEdges(rawEdges);
    } catch (error) {
      console.error("Failed to fetch map data", error);
    }
  }, [repoId, setNodes, setEdges]);

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
