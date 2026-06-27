import React, { useState } from 'react';

export default function ReviewCenterLayout() {
  const [reviews] = useState([
    { id: 'rev-1', entity: 'Electric Arc Furnace', type: 'equipment', author: 'u-engineer', status: 'PENDING', ai_score: '98%', risk: 'LOW' },
    { id: 'rev-2', entity: 'EAF High Voltage Protocol', type: 'sop', author: 'u-operator', status: 'PENDING', ai_score: '65%', risk: 'HIGH' }
  ]);

  return (
    <div style={{ padding: '24px', color: 'white', height: '100%', overflowY: 'auto' }}>
      <header style={{ marginBottom: '32px' }}>
        <h1 style={{ margin: '0 0 8px 0' }}>Review Center</h1>
        <p style={{ color: '#a0aec0', margin: 0 }}>Review and approve pending knowledge drafts before publication.</p>
      </header>

      <div style={{ display: 'grid', gap: '16px' }}>
        {reviews.map(rev => (
          <div key={rev.id} style={{ background: '#1a1d24', border: '1px solid #2d3748', borderRadius: '8px', padding: '16px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <h3 style={{ margin: '0 0 4px 0' }}>{rev.entity}</h3>
              <p style={{ margin: 0, color: '#a0aec0', fontSize: '12px' }}>Type: {rev.type} | Submitted by: {rev.author}</p>
            </div>
            
            <div style={{ display: 'flex', gap: '24px', alignItems: 'center' }}>
              <div style={{ textAlign: 'right' }}>
                <div style={{ fontSize: '12px', color: '#a0aec0' }}>AI Completeness</div>
                <div style={{ color: rev.ai_score === '98%' ? '#48bb78' : '#ecc94b', fontWeight: 'bold' }}>{rev.ai_score}</div>
              </div>
              <div style={{ textAlign: 'right' }}>
                <div style={{ fontSize: '12px', color: '#a0aec0' }}>Risk Score</div>
                <div style={{ color: rev.risk === 'LOW' ? '#48bb78' : '#f56565', fontWeight: 'bold' }}>{rev.risk}</div>
              </div>
              <div style={{ display: 'flex', gap: '8px' }}>
                <button style={{ background: '#38a169', color: 'white', border: 'none', padding: '8px 16px', borderRadius: '4px', cursor: 'pointer' }}>Approve</button>
                <button style={{ background: '#e53e3e', color: 'white', border: 'none', padding: '8px 16px', borderRadius: '4px', cursor: 'pointer' }}>Reject</button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
