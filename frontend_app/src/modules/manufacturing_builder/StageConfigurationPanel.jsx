import React from 'react';

export default function StageConfigurationPanel({ selectedNode }) {
  if (!selectedNode) {
    return (
      <div style={{ padding: '24px', color: '#a0aec0', textAlign: 'center' }}>
        Select a stage on the canvas to configure it.
      </div>
    );
  }

  return (
    <div style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '20px' }}>
      <header>
        <h3 style={{ margin: '0 0 8px 0', color: '#fff' }}>Stage Configuration</h3>
        <p style={{ margin: 0, color: '#a0aec0', fontSize: '14px' }}>Configure metadata and AI rules.</p>
      </header>

      <div style={{ background: '#2d3748', padding: '16px', borderRadius: '8px' }}>
        <h4 style={{ margin: '0 0 12px 0', color: '#63b3ed' }}>Node: {selectedNode.data.label}</h4>
        
        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
            <label style={{ fontSize: '12px', color: '#a0aec0' }}>Estimated Duration (mins)</label>
            <input type="number" defaultValue={120} style={inputStyle} />
          </div>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
            <label style={{ fontSize: '12px', color: '#a0aec0' }}>Required SOPs (Comma separated IDs)</label>
            <input type="text" placeholder="sop-01, sop-05" style={inputStyle} />
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
            <label style={{ fontSize: '12px', color: '#a0aec0' }}>Required PPE</label>
            <input type="text" placeholder="Hard Hat, Safety Glasses" style={inputStyle} />
          </div>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
            <label style={{ fontSize: '12px', color: '#a0aec0' }}>Quality Checks</label>
            <input type="text" placeholder="Temp Check, Chemical Analysis" style={inputStyle} />
          </div>
        </div>
      </div>
      
      <div style={{ background: '#2a2618', border: '1px solid #b7791f', padding: '16px', borderRadius: '8px' }}>
        <h4 style={{ margin: '0 0 8px 0', color: '#ecc94b', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span>✨</span> AI Assistance
        </h4>
        <p style={{ fontSize: '13px', color: '#d69e2e', margin: 0 }}>
          <strong>Missing Link:</strong> This stage has no Equipment mapped. Are you sure it's a manual stage?
        </p>
      </div>

    </div>
  );
}

const inputStyle = {
  background: '#1a202c', border: '1px solid #4a5568', color: '#fff', padding: '8px', borderRadius: '4px'
};
