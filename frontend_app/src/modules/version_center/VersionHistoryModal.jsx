import React from 'react';

export default function VersionHistoryModal({ onClose }) {
  const versions = [
    { v: 'v1.1.0', date: '2024-10-12', author: 'System', notes: 'Added missing SOP relationships', ai_summary: 'Graph relationships expanded.' },
    { v: 'v1.0.0', date: '2024-10-10', author: 'u-engineer', notes: 'Initial publication', ai_summary: 'Entity created.' }
  ];

  return (
    <div style={{ 
      position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, 
      background: 'rgba(0,0,0,0.8)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000 
    }}>
      <div style={{ background: '#1a1d24', width: '800px', borderRadius: '8px', border: '1px solid #2d3748', display: 'flex', flexDirection: 'column', maxHeight: '90vh' }}>
        
        <header style={{ padding: '24px', borderBottom: '1px solid #2d3748', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h2 style={{ margin: 0, color: 'white' }}>Version History: Jajpur Plant</h2>
          <button onClick={onClose} style={{ background: 'transparent', border: 'none', color: '#a0aec0', cursor: 'pointer', fontSize: '20px' }}>×</button>
        </header>

        <div style={{ padding: '24px', overflowY: 'auto', flex: 1 }}>
          
          <div style={{ display: 'flex', gap: '24px', marginBottom: '32px' }}>
            <div style={{ flex: 1, background: '#111318', padding: '16px', borderRadius: '8px', border: '1px solid #4a5568' }}>
              <h4 style={{ color: '#f56565', margin: '0 0 16px 0' }}>v1.0.0 (Previous)</h4>
              <pre style={{ color: '#a0aec0', fontSize: '12px', margin: 0 }}>
                {`{
  "name": "Jajpur Plant",
  "metadata": {
    "location": "Odisha"
  }
}`}
              </pre>
            </div>
            <div style={{ flex: 1, background: '#111318', padding: '16px', borderRadius: '8px', border: '1px solid #48bb78' }}>
              <h4 style={{ color: '#48bb78', margin: '0 0 16px 0' }}>v1.1.0 (Current)</h4>
              <pre style={{ color: '#a0aec0', fontSize: '12px', margin: 0 }}>
                {`{
  "name": "Jajpur Plant",
  "metadata": {
    "location": "Odisha",
+   "capacity": "1.5 MTPA"
  }
}`}
              </pre>
            </div>
          </div>

          <h3 style={{ color: 'white', marginBottom: '16px' }}>Timeline</h3>
          <div style={{ borderLeft: '2px solid #2d3748', paddingLeft: '16px' }}>
            {versions.map(v => (
              <div key={v.v} style={{ marginBottom: '24px', position: 'relative' }}>
                <div style={{ position: 'absolute', left: '-21px', top: '4px', width: '10px', height: '10px', background: '#3182ce', borderRadius: '50%' }}></div>
                <h4 style={{ color: 'white', margin: '0 0 4px 0' }}>{v.v} - {v.notes}</h4>
                <p style={{ color: '#a0aec0', margin: '0 0 8px 0', fontSize: '12px' }}>{v.date} | By: {v.author}</p>
                <p style={{ color: '#ecc94b', margin: 0, fontSize: '13px' }}>✨ AI Summary: {v.ai_summary}</p>
                <div style={{ marginTop: '8px' }}>
                  <button style={{ background: 'transparent', border: '1px solid #e53e3e', color: '#e53e3e', padding: '4px 8px', borderRadius: '4px', fontSize: '12px', cursor: 'pointer' }}>Rollback to this version</button>
                </div>
              </div>
            ))}
          </div>

        </div>
      </div>
    </div>
  );
}
