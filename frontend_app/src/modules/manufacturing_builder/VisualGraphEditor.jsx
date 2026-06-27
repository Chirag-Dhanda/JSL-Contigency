import React, { useCallback } from 'react';
import {
  ReactFlow,
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
} from 'reactflow';
import 'reactflow/dist/style.css';

const initialNodes = [
  { id: '1', position: { x: 250, y: 5 }, data: { label: 'Scrap Yard / Sorting' } },
  { id: '2', position: { x: 250, y: 150 }, data: { label: 'Electric Arc Furnace (EAF)' } },
  { id: '3', position: { x: 250, y: 300 }, data: { label: 'Argon Oxygen Decarburization (AOD)' } },
];

const initialEdges = [
  { id: 'e1-2', source: '1', target: '2', animated: true, label: 'NEXT_STAGE' },
  { id: 'e2-3', source: '2', target: '3', animated: true, label: 'NEXT_STAGE' }
];

export default function VisualGraphEditor({ onNodeClick }) {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge(params, eds)),
    [setEdges],
  );

  return (
    <div style={{ width: '100%', height: '100%' }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        onNodeClick={(_, node) => onNodeClick(node)}
        fitView
      >
        <Controls />
        <MiniMap nodeColor={(node) => {
          return '#3182ce';
        }} />
        <Background variant="dots" gap={12} size={1} />
      </ReactFlow>
    </div>
  );
}
