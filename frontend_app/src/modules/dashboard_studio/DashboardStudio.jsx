import React from 'react';

export default function DashboardStudio() {
  return (
    <div style={{ padding: '24px', color: 'white', height: '100%', overflowY: 'auto' }}>
      <header style={{ marginBottom: '32px' }}>
        <h1 style={{ margin: '0 0 8px 0' }}>Dashboard Studio</h1>
        <p style={{ color: '#a0aec0', margin: 0 }}>Configure personalized workspaces for different enterprise roles.</p>
      </header>

      <div style={{ display: 'flex', gap: '24px' }}>
        
        {/* Templates List */}
        <div style={{ width: '300px', background: '#1a1d24', border: '1px solid #2d3748', borderRadius: '8px', padding: '16px' }}>
          <h3 style={{ margin: '0 0 16px 0', fontSize: '16px' }}>Role Templates</h3>
          <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
            <li style={{ padding: '12px', background: '#2b6cb0', borderRadius: '4px', cursor: 'pointer', marginBottom: '8px' }}>Engineer Workspace</li>
            <li style={{ padding: '12px', background: 'transparent', borderRadius: '4px', cursor: 'pointer', marginBottom: '8px', color: '#a0aec0' }}>Operator Workspace</li>
            <li style={{ padding: '12px', background: 'transparent', borderRadius: '4px', cursor: 'pointer', color: '#a0aec0' }}>Master Editor Workspace</li>
          </ul>
        </div>

        {/* Visual Builder Mock */}
        <div style={{ flex: 1, background: '#1a1d24', border: '1px solid #2d3748', borderRadius: '8px', padding: '24px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '24px' }}>
            <h2>Engineer Workspace Layout</h2>
            <button style={{ background: '#38a169', color: 'white', border: 'none', padding: '8px 16px', borderRadius: '4px' }}>Save Changes</button>
          </div>
          
          <div style={{ 
            background: '#111318', border: '2px dashed #4a5568', borderRadius: '8px', padding: '24px',
            display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '16px'
          }}>
            <div style={{ gridColumn: 'span 2', height: '150px', background: '#2d3748', display: 'flex', alignItems: 'center', justifyContent: 'center', borderRadius: '4px' }}>Assigned Equipment Widget</div>
            <div style={{ gridColumn: 'span 1', height: '150px', background: '#2d3748', display: 'flex', alignItems: 'center', justifyContent: 'center', borderRadius: '4px' }}>Learning Progress Widget</div>
            <div style={{ gridColumn: 'span 1', height: '150px', background: '#2d3748', display: 'flex', alignItems: 'center', justifyContent: 'center', borderRadius: '4px' }}>Announcements Widget</div>
            <div style={{ gridColumn: 'span 2', height: '150px', background: '#4a5568', border: '2px dashed #a0aec0', display: 'flex', alignItems: 'center', justifyContent: 'center', borderRadius: '4px', cursor: 'pointer', color: '#a0aec0' }}>+ Drag Widget Here</div>
          </div>
        </div>

      </div>
    </div>
  );
}
