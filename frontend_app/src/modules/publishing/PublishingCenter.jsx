import React, { useState } from 'react';
import VersionHistoryModal from '../version_center/VersionHistoryModal';

export default function PublishingCenter() {
  const [showVersions, setShowVersions] = useState(false);
  
  const [drafts] = useState([
    { id: 'ent-1', name: 'Jajpur Plant', state: 'APPROVED', impact: 'HIGH', versions: 5 },
    { id: 'ent-2', name: 'EAF Safety Protocol', state: 'DRAFT', impact: 'LOW', versions: 1 }
  ]);

  return (
    <div style={{ padding: '24px', color: 'white', height: '100%', overflowY: 'auto' }}>
      <header style={{ marginBottom: '32px' }}>
        <h1 style={{ margin: '0 0 8px 0' }}>Publishing Center</h1>
        <p style={{ color: '#a0aec0', margin: 0 }}>Manage the lifecycle and publication of approved enterprise entities.</p>
      </header>

      <div style={{ background: '#1a1d24', border: '1px solid #2d3748', borderRadius: '8px' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ borderBottom: '1px solid #2d3748', textAlign: 'left', color: '#a0aec0', fontSize: '12px', textTransform: 'uppercase' }}>
              <th style={{ padding: '16px' }}>Entity</th>
              <th style={{ padding: '16px' }}>State</th>
              <th style={{ padding: '16px' }}>Change Impact</th>
              <th style={{ padding: '16px' }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {drafts.map(draft => (
              <tr key={draft.id} style={{ borderBottom: '1px solid #2d3748' }}>
                <td style={{ padding: '16px', fontWeight: 'bold' }}>
                  {draft.name}
                  <div style={{ fontSize: '12px', color: '#63b3ed', cursor: 'pointer', marginTop: '4px' }} onClick={() => setShowVersions(true)}>
                    View History ({draft.versions} versions)
                  </div>
                </td>
                <td style={{ padding: '16px' }}>
                  <span style={{ 
                    padding: '4px 8px', borderRadius: '4px', fontSize: '12px',
                    background: draft.state === 'APPROVED' ? 'rgba(72,187,120,0.2)' : 'rgba(160,174,192,0.2)',
                    color: draft.state === 'APPROVED' ? '#48bb78' : '#a0aec0'
                  }}>
                    {draft.state}
                  </span>
                </td>
                <td style={{ padding: '16px' }}>
                  <span style={{ color: draft.impact === 'HIGH' ? '#f56565' : '#48bb78' }}>
                    {draft.impact}
                  </span>
                </td>
                <td style={{ padding: '16px' }}>
                  <button 
                    disabled={draft.state !== 'APPROVED'}
                    style={{ 
                      background: draft.state === 'APPROVED' ? '#3182ce' : '#2d3748', 
                      color: draft.state === 'APPROVED' ? 'white' : '#a0aec0', 
                      border: 'none', padding: '8px 16px', borderRadius: '4px', cursor: draft.state === 'APPROVED' ? 'pointer' : 'not-allowed' 
                    }}>
                    Publish Now
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      
      {showVersions && <VersionHistoryModal onClose={() => setShowVersions(false)} />}
    </div>
  );
}
