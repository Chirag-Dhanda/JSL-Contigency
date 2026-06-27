import React, { useState } from 'react';
import { Routes, Route, Link, useLocation } from 'react-router-dom';
import './App.css';
import PerformanceDashboard from './components/PerformanceDashboard';
import OrchestratorDashboard from './components/OrchestratorDashboard';
import UnifiedHealthDashboard from './components/UnifiedHealthDashboard';
import KnowledgeStudioLayout from './modules/knowledge_studio/KnowledgeStudioLayout';

function StandardApp() {
  const [activeTab, setActiveTab] = useState('health');

  const mockMetrics = {
    cache_hit_rate_percent: 45.2,
    median_latency_ms: 120
  };

  const mockAgents = [
    { agent_id: 'mfg_expert', name: 'Manufacturing Expert', status: 'Online', capabilities: ['specs', 'troubleshooting'], priority: 10 },
    { agent_id: 'safety_expert', name: 'Safety Expert', status: 'Online', capabilities: ['ppe', 'loto'], priority: 100 }
  ];

  const mockHistory = [
    { query: "What is the max equipment spec for the EAF?", agents_used: ['mfg_expert'], merged_sources: ['EQ-SPEC-01'] }
  ];

  const mockHealthData = {
    status: 'Healthy',
    components: {
      enterprise_gateway: 'Online',
      ollama_local: 'Online',
      chromadb_vector: 'Online',
      embedding_service: 'Online',
      AI_Facade: 'Online',
      Runtime_Engine: 'Online',
      Agent_Registry: 'Online'
    },
    metrics: mockMetrics
  };

  return (
    <div style={{ background: '#1a202c', minHeight: '100vh' }}>
      <nav style={{ padding: '16px', background: '#2d3748', display: 'flex', gap: '16px', borderBottom: '1px solid #4a5568', alignItems: 'center' }}>
        <button 
          onClick={() => setActiveTab('health')} 
          style={{ background: activeTab === 'health' ? '#3182ce' : '#4a5568', color: 'white', border: 'none', padding: '8px 16px', borderRadius: '4px', cursor: 'pointer', fontWeight: 'bold' }}
        >
          Unified System Health
        </button>
        <button 
          onClick={() => setActiveTab('performance')} 
          style={{ background: activeTab === 'performance' ? '#3182ce' : '#4a5568', color: 'white', border: 'none', padding: '8px 16px', borderRadius: '4px', cursor: 'pointer' }}
        >
          Performance Monitoring
        </button>
        <button 
          onClick={() => setActiveTab('orchestrator')} 
          style={{ background: activeTab === 'orchestrator' ? '#3182ce' : '#4a5568', color: 'white', border: 'none', padding: '8px 16px', borderRadius: '4px', cursor: 'pointer' }}
        >
          AI Orchestrator
        </button>
        <div style={{ flex: 1 }}></div>
        <Link to="/studio" style={{ color: '#63b3ed', textDecoration: 'none', fontWeight: 'bold' }}>Go to Knowledge Studio ➔</Link>
      </nav>

      {activeTab === 'health' && (
        <UnifiedHealthDashboard healthData={mockHealthData} />
      )}

      {activeTab === 'performance' && (
        <PerformanceDashboard 
          metricsData={mockMetrics} 
          queueDepth={8} 
          circuitBreakerStatus="Closed" 
        />
      )}

      {activeTab === 'orchestrator' && (
        <OrchestratorDashboard 
          registeredAgents={mockAgents} 
          executionHistory={mockHistory} 
        />
      )}
    </div>
  );
}

function App() {
  const [currentUser, setCurrentUser] = useState({ username: 'guest', role: 'LEARNER' });

  return (
    <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      {/* MOCK LOGIN BAR */}
      <div style={{ background: '#000', color: '#fff', padding: '8px 16px', display: 'flex', gap: '16px', alignItems: 'center', fontSize: '14px' }}>
        <span>Current User: <strong>{currentUser.username}</strong> ({currentUser.role})</span>
        <button 
          onClick={() => setCurrentUser({ username: 'guest', role: 'LEARNER' })}
          style={{ background: currentUser.username === 'guest' ? '#48bb78' : '#4a5568', color: 'white', border: 'none', padding: '4px 8px', borderRadius: '4px', cursor: 'pointer' }}
        >
          Login as Learner
        </button>
        <button 
          onClick={() => setCurrentUser({ username: 'master_editor_demo', role: 'MASTER_EDITOR' })}
          style={{ background: currentUser.username === 'master_editor_demo' ? '#48bb78' : '#4a5568', color: 'white', border: 'none', padding: '4px 8px', borderRadius: '4px', cursor: 'pointer' }}
        >
          Login as Master Editor
        </button>
      </div>

      <div style={{ flex: 1 }}>
        <Routes>
          <Route path="/studio/*" element={
            currentUser.role === 'MASTER_EDITOR' 
              ? <KnowledgeStudioLayout /> 
              : <div style={{ padding: '40px', color: 'white', textAlign: 'center', background: '#1a202c', minHeight: '100vh' }}>
                  <h2>Access Denied</h2>
                  <p>You do not have the MASTER_EDITOR role required to access the Knowledge Studio.</p>
                  <Link to="/" style={{ color: '#63b3ed' }}>Return to Dashboard</Link>
                </div>
          } />
          <Route path="/*" element={<StandardApp />} />
        </Routes>
      </div>
    </div>
  );
}

export default App;
