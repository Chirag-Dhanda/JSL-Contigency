import React from 'react';

const UnifiedHealthDashboard = ({ healthData }) => {
  if (!healthData) return null;

  return (
    <div style={{ padding: '24px', background: '#1a202c', color: '#e2e8f0', minHeight: '100vh', fontFamily: 'sans-serif' }}>
      <header style={{ marginBottom: '32px' }}>
        <h1 style={{ fontSize: '2rem', margin: 0 }}>Enterprise AI Platform Health</h1>
        <p style={{ color: '#a0aec0', marginTop: '8px' }}>Unified System Monitor</p>
      </header>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '24px' }}>
        
        {/* Core Services Widget */}
        <div style={{ background: '#2d3748', padding: '20px', borderRadius: '12px' }}>
          <h2 style={{ fontSize: '1.25rem', marginTop: 0, color: '#63b3ed' }}>Core Services</h2>
          <ul style={{ listStyleType: 'none', padding: 0, marginTop: '16px' }}>
            <li style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
              <span style={{ color: '#a0aec0' }}>Frontend App</span>
              <span style={{ color: '#48bb78', fontWeight: 'bold' }}>Online</span>
            </li>
            <li style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
              <span style={{ color: '#a0aec0' }}>Backend API</span>
              <span style={{ color: '#48bb78', fontWeight: 'bold' }}>Online</span>
            </li>
            <li style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
              <span style={{ color: '#a0aec0' }}>Enterprise Gateway</span>
              <span style={{ color: healthData.components.enterprise_gateway === 'Online' ? '#48bb78' : '#fc8181', fontWeight: 'bold' }}>
                {healthData.components.enterprise_gateway || 'Offline'}
              </span>
            </li>
          </ul>
        </div>

        {/* Inference Engine Widget */}
        <div style={{ background: '#2d3748', padding: '20px', borderRadius: '12px' }}>
          <h2 style={{ fontSize: '1.25rem', marginTop: 0, color: '#f6ad55' }}>Inference & Embeddings</h2>
          <ul style={{ listStyleType: 'none', padding: 0, marginTop: '16px' }}>
            <li style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
              <span style={{ color: '#a0aec0' }}>Ollama Local</span>
              <span style={{ color: healthData.components.ollama_local === 'Online' ? '#48bb78' : '#fc8181', fontWeight: 'bold' }}>
                {healthData.components.ollama_local || 'Offline'}
              </span>
            </li>
            <li style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
              <span style={{ color: '#a0aec0' }}>Embedding Service</span>
              <span style={{ color: healthData.components.embedding_service === 'Online' ? '#48bb78' : '#fc8181', fontWeight: 'bold' }}>
                {healthData.components.embedding_service || 'Offline'}
              </span>
            </li>
            <li style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
              <span style={{ color: '#a0aec0' }}>ChromaDB Vector</span>
              <span style={{ color: healthData.components.chromadb_vector === 'Online' ? '#48bb78' : '#fc8181', fontWeight: 'bold' }}>
                {healthData.components.chromadb_vector || 'Offline'}
              </span>
            </li>
          </ul>
        </div>

        {/* Runtime & Orchestrator Widget */}
        <div style={{ background: '#2d3748', padding: '20px', borderRadius: '12px' }}>
          <h2 style={{ fontSize: '1.25rem', marginTop: 0, color: '#9f7aea' }}>Runtime & Orchestration</h2>
          <ul style={{ listStyleType: 'none', padding: 0, marginTop: '16px' }}>
            <li style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
              <span style={{ color: '#a0aec0' }}>AI Facade</span>
              <span style={{ color: healthData.components.AI_Facade === 'Online' ? '#48bb78' : '#fc8181', fontWeight: 'bold' }}>
                {healthData.components.AI_Facade || 'Offline'}
              </span>
            </li>
            <li style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
              <span style={{ color: '#a0aec0' }}>Runtime Engine</span>
              <span style={{ color: healthData.components.Runtime_Engine === 'Online' ? '#48bb78' : '#fc8181', fontWeight: 'bold' }}>
                {healthData.components.Runtime_Engine || 'Offline'}
              </span>
            </li>
            <li style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
              <span style={{ color: '#a0aec0' }}>Agent Registry</span>
              <span style={{ color: healthData.components.Agent_Registry === 'Online' ? '#48bb78' : '#fc8181', fontWeight: 'bold' }}>
                {healthData.components.Agent_Registry || 'Offline'}
              </span>
            </li>
          </ul>
        </div>

      </div>

      <div style={{ marginTop: '32px', textAlign: 'center', padding: '20px', background: healthData.status === 'Healthy' ? '#22543d' : '#742a2a', borderRadius: '12px' }}>
        <h2 style={{ margin: 0, color: healthData.status === 'Healthy' ? '#9ae6b4' : '#fc8181' }}>
          OVERALL PLATFORM STATUS: {healthData.status.toUpperCase()}
        </h2>
      </div>
    </div>
  );
};

export default UnifiedHealthDashboard;
