import React from 'react';

const PerformanceDashboard = ({ metricsData, queueDepth, circuitBreakerStatus }) => {
  if (!metricsData) return null;

  return (
    <div style={{ padding: '24px', background: '#1a202c', color: '#e2e8f0', minHeight: '100vh', fontFamily: 'sans-serif' }}>
      <header style={{ marginBottom: '32px' }}>
        <h1 style={{ fontSize: '2rem', margin: 0 }}>Performance & Reliability</h1>
        <p style={{ color: '#a0aec0', marginTop: '8px' }}>Enterprise AI Runtime Monitoring</p>
      </header>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '24px' }}>
        
        {/* Runtime Metrics Widget */}
        <div style={{ background: '#2d3748', padding: '20px', borderRadius: '12px' }}>
          <h2 style={{ fontSize: '1.25rem', marginTop: 0, color: '#48bb78' }}>Runtime Metrics</h2>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginTop: '16px' }}>
            <div style={{ background: '#1a202c', padding: '12px', borderRadius: '8px' }}>
              <span style={{ color: '#a0aec0', fontSize: '0.85rem' }}>Cache Hit Rate</span>
              <strong style={{ display: 'block', fontSize: '1.5rem', marginTop: '4px', color: '#63b3ed' }}>
                {metricsData.cache_hit_rate_percent.toFixed(1)}%
              </strong>
            </div>
            <div style={{ background: '#1a202c', padding: '12px', borderRadius: '8px' }}>
              <span style={{ color: '#a0aec0', fontSize: '0.85rem' }}>Median Latency</span>
              <strong style={{ display: 'block', fontSize: '1.5rem', marginTop: '4px' }}>
                {metricsData.median_latency_ms}ms
              </strong>
            </div>
          </div>
        </div>

        {/* Traffic Control Widget */}
        <div style={{ background: '#2d3748', padding: '20px', borderRadius: '12px' }}>
          <h2 style={{ fontSize: '1.25rem', marginTop: 0, color: '#ed8936' }}>Traffic Control</h2>
          <div style={{ marginTop: '16px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
              <span style={{ color: '#a0aec0' }}>Queue Depth</span>
              <span style={{ color: queueDepth > 15 ? '#fc8181' : queueDepth > 5 ? '#fbd38d' : '#48bb78', fontWeight: 'bold' }}>
                {queueDepth} / 20
              </span>
            </div>
            <div style={{ background: '#4a5568', height: '8px', borderRadius: '4px', marginTop: '8px' }}>
              <div style={{ 
                background: queueDepth > 15 ? '#fc8181' : queueDepth > 5 ? '#fbd38d' : '#48bb78', 
                width: `${(queueDepth / 20) * 100}%`, 
                height: '100%', 
                borderRadius: '4px' 
              }}></div>
            </div>
          </div>
        </div>

        {/* Fault Tolerance Widget */}
        <div style={{ background: '#2d3748', padding: '20px', borderRadius: '12px' }}>
          <h2 style={{ fontSize: '1.25rem', marginTop: 0, color: '#fc8181' }}>Fault Tolerance</h2>
          <div style={{ marginTop: '16px', background: '#1a202c', padding: '16px', borderRadius: '8px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ color: '#a0aec0' }}>Main Circuit Breaker</span>
              <span style={{ 
                background: circuitBreakerStatus === 'Open' ? '#742a2a' : '#22543d', 
                color: circuitBreakerStatus === 'Open' ? '#fc8181' : '#9ae6b4', 
                padding: '4px 12px', 
                borderRadius: '4px', 
                fontWeight: 'bold' 
              }}>
                {circuitBreakerStatus}
              </span>
            </div>
            {circuitBreakerStatus === 'Open' && (
              <p style={{ marginTop: '12px', color: '#fed7d7', fontSize: '0.85rem' }}>
                Traffic halted. Failing fast to prevent cascading system failure.
              </p>
            )}
          </div>
        </div>

      </div>
    </div>
  );
};

export default PerformanceDashboard;
