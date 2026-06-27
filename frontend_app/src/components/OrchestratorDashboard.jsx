import React, { useState } from 'react';

const OrchestratorDashboard = ({ registeredAgents, executionHistory }) => {
  const [activeTab, setActiveTab] = useState('registry');

  return (
    <div style={{ padding: '24px', background: '#1a202c', color: '#e2e8f0', minHeight: '100vh', fontFamily: 'sans-serif' }}>
      <header style={{ marginBottom: '32px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h1 style={{ fontSize: '2rem', margin: 0 }}>AI Orchestrator</h1>
          <p style={{ color: '#a0aec0', marginTop: '8px' }}>Enterprise Multi-Agent Coordination</p>
        </div>
        <div>
          <button onClick={() => setActiveTab('registry')} style={{ background: activeTab === 'registry' ? '#2b6cb0' : '#4a5568', color: 'white', border: 'none', padding: '8px 16px', borderRadius: '4px', marginRight: '8px', cursor: 'pointer' }}>Agent Registry</button>
          <button onClick={() => setActiveTab('executions')} style={{ background: activeTab === 'executions' ? '#2b6cb0' : '#4a5568', color: 'white', border: 'none', padding: '8px 16px', borderRadius: '4px', cursor: 'pointer' }}>Execution Monitoring</button>
        </div>
      </header>

      {activeTab === 'registry' && (
        <div>
          <h2 style={{ fontSize: '1.25rem', color: '#63b3ed', marginBottom: '16px' }}>Registered Agents</h2>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '24px' }}>
            {registeredAgents.map((agent) => (
              <div key={agent.agent_id} style={{ background: '#2d3748', padding: '20px', borderRadius: '12px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <h3 style={{ margin: 0, color: '#e2e8f0' }}>{agent.name}</h3>
                  <span style={{ 
                    background: agent.status === 'Online' ? '#22543d' : '#742a2a', 
                    color: agent.status === 'Online' ? '#9ae6b4' : '#fc8181', 
                    padding: '4px 8px', borderRadius: '4px', fontSize: '0.75rem', textTransform: 'uppercase' 
                  }}>
                    {agent.status}
                  </span>
                </div>
                
                <div style={{ marginTop: '16px' }}>
                  <span style={{ fontSize: '0.8rem', color: '#a0aec0' }}>Capabilities:</span>
                  <div style={{ display: 'flex', gap: '8px', marginTop: '8px', flexWrap: 'wrap' }}>
                    {agent.capabilities.map(cap => (
                      <span key={cap} style={{ background: '#4a5568', padding: '2px 8px', borderRadius: '4px', fontSize: '0.75rem', color: '#cbd5e0' }}>{cap}</span>
                    ))}
                  </div>
                </div>

                <div style={{ marginTop: '16px', borderTop: '1px solid #4a5568', paddingTop: '12px', display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', color: '#a0aec0' }}>
                  <span>ID: {agent.agent_id}</span>
                  <span>Priority: {agent.priority}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {activeTab === 'executions' && (
        <div style={{ background: '#2d3748', padding: '24px', borderRadius: '12px' }}>
          <h2 style={{ fontSize: '1.25rem', color: '#ed8936', marginTop: 0 }}>Recent Executions</h2>
          
          <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '16px', fontSize: '0.9rem' }}>
            <thead>
              <tr style={{ textAlign: 'left', color: '#a0aec0', borderBottom: '1px solid #4a5568' }}>
                <th style={{ padding: '12px 8px' }}>Query</th>
                <th style={{ padding: '12px 8px' }}>Agents Invoked</th>
                <th style={{ padding: '12px 8px' }}>Aggregated Sources</th>
                <th style={{ padding: '12px 8px' }}>Status</th>
              </tr>
            </thead>
            <tbody>
              {executionHistory.map((exec, idx) => (
                <tr key={idx} style={{ borderBottom: '1px solid #4a5568' }}>
                  <td style={{ padding: '12px 8px', color: '#e2e8f0', maxWidth: '300px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{exec.query}</td>
                  <td style={{ padding: '12px 8px', color: '#cbd5e0' }}>{exec.agents_used.join(', ')}</td>
                  <td style={{ padding: '12px 8px', color: '#63b3ed' }}>{exec.merged_sources.length} sources</td>
                  <td style={{ padding: '12px 8px', color: '#48bb78' }}>Success</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default OrchestratorDashboard;
