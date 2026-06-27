import React from 'react';

// Core Widget Components
const SystemStatsWidget = () => (
  <div style={{ padding: '16px', background: '#2c7a7b', borderRadius: '8px', color: 'white', height: '100%' }}>
    <h3 style={{ margin: '0 0 16px 0' }}>📈 Platform Health</h3>
    <div style={{ display: 'flex', justifyContent: 'space-around' }}>
      <div style={{ textAlign: 'center' }}><h2>4,204</h2><p>Nodes</p></div>
      <div style={{ textAlign: 'center' }}><h2>18,502</h2><p>Edges</p></div>
      <div style={{ textAlign: 'center' }}><h2>99.9%</h2><p>Uptime</p></div>
    </div>
  </div>
);

const AnnouncementsWidget = () => (
  <div style={{ padding: '16px', background: '#2d3748', borderRadius: '8px', color: 'white', height: '100%', border: '1px solid #4a5568' }}>
    <h3 style={{ margin: '0 0 16px 0', color: '#ecc94b' }}>📣 Company Announcements</h3>
    <ul style={{ paddingLeft: '20px', margin: 0, color: '#e2e8f0' }}>
      <li style={{ marginBottom: '8px' }}>Q3 Safety Audit scheduled for next week.</li>
      <li>New EAF training module available.</li>
    </ul>
  </div>
);

const LearningProgressWidget = () => (
  <div style={{ padding: '16px', background: '#1a365d', borderRadius: '8px', color: 'white', height: '100%' }}>
    <h3 style={{ margin: '0 0 16px 0' }}>🎓 My Training</h3>
    <p style={{ margin: '0 0 8px 0', fontSize: '14px' }}>Arc Furnace Safety (In Progress)</p>
    <div style={{ background: '#2b6cb0', height: '8px', borderRadius: '4px', width: '100%' }}>
      <div style={{ background: '#63b3ed', height: '100%', width: '60%', borderRadius: '4px' }}></div>
    </div>
    <p style={{ margin: '8px 0 0 0', fontSize: '12px', textAlign: 'right' }}>60%</p>
  </div>
);

const QuickActionsWidget = ({ config }) => {
  const actions = config.settings?.actions || ["search", "copilot"];
  return (
    <div style={{ padding: '16px', background: '#2d3748', borderRadius: '8px', color: 'white', height: '100%', border: '1px solid #4a5568' }}>
      <h3 style={{ margin: '0 0 16px 0' }}>⚡ Quick Actions</h3>
      <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
        {actions.map(act => (
          <button key={act} style={{ background: '#4a5568', color: 'white', border: 'none', padding: '8px 12px', borderRadius: '4px', cursor: 'pointer', flex: 1, minWidth: '80px', textTransform: 'capitalize' }}>
            {act}
          </button>
        ))}
      </div>
    </div>
  );
};

const DefaultWidget = ({ config }) => (
  <div style={{ padding: '16px', background: '#2d3748', borderRadius: '8px', color: 'white', height: '100%', border: '1px solid #4a5568', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
    <p style={{ color: '#a0aec0' }}>Widget: {config.title} (Placeholder)</p>
  </div>
);

export const WidgetRegistry = {
  renderWidget: (config) => {
    switch (config.type) {
      case 'system_stats': return <SystemStatsWidget key={config.id} />;
      case 'announcements': return <AnnouncementsWidget key={config.id} />;
      case 'learning_progress': return <LearningProgressWidget key={config.id} />;
      case 'quick_actions': return <QuickActionsWidget key={config.id} config={config} />;
      default: return <DefaultWidget key={config.id} config={config} />;
    }
  }
};
