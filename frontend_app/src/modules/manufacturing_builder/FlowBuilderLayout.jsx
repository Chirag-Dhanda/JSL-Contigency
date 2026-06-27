import React, { useState } from 'react';
import VisualGraphEditor from './VisualGraphEditor';
import StageConfigurationPanel from './StageConfigurationPanel';
import { ReactFlowProvider } from 'reactflow';

export default function FlowBuilderLayout() {
  const [selectedNode, setSelectedNode] = useState(null);

  return (
    <div className="ks-page" style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      <header style={{ marginBottom: '24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h1 style={{ margin: '0 0 8px 0', color: '#fff' }}>Manufacturing Flow Builder</h1>
          <p style={{ margin: 0, color: '#a0aec0' }}>Visually model plant structures and automatically generate Knowledge Graph relationships.</p>
        </div>
        <button style={{ background: '#38a169', color: 'white', padding: '10px 20px', border: 'none', borderRadius: '4px', fontWeight: 'bold', cursor: 'pointer' }}>
          Publish Flow to Runtime
        </button>
      </header>
      
      <div style={{ display: 'flex', flex: 1, gap: '24px', overflow: 'hidden' }}>
        {/* LEFT: Canvas */}
        <div style={{ flex: 3, background: '#1a1d24', borderRadius: '8px', border: '1px solid #2d3748', overflow: 'hidden' }}>
          <ReactFlowProvider>
            <VisualGraphEditor onNodeClick={setSelectedNode} />
          </ReactFlowProvider>
        </div>
        
        {/* RIGHT: Sidebar */}
        <div style={{ flex: 1, background: '#1a1d24', borderRadius: '8px', border: '1px solid #2d3748', overflowY: 'auto' }}>
          <StageConfigurationPanel selectedNode={selectedNode} />
        </div>
      </div>
    </div>
  );
}
