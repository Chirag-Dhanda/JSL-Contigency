import React, { useState, useEffect } from 'react';
import { WidgetRegistry } from '../widget_engine/WidgetRegistry';

export default function WorkspaceLayout() {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [role, setRole] = useState("ENGINEER"); // Mock active role toggle

  useEffect(() => {
    setLoading(true);
    
    // Simulating API call to fetch personalized workspace profile
    setTimeout(() => {
      // Mocked Backend Response
      let layoutWidgets = [];
      let recs = [];
      
      if (role === "MASTER_EDITOR") {
        layoutWidgets = [
          { id: "w1", type: "system_stats", title: "Platform Health", grid_area: "span 1 / span 3" },
          { id: "w2", type: "pending_reviews", title: "Pending AI Intake Reviews", grid_area: "span 2 / span 2" },
          { id: "w3", type: "quick_actions", title: "Quick Actions", grid_area: "span 1 / span 1", settings: { actions: ["upload", "studio", "users"] } }
        ];
        recs = [
          { id: "r1", title: "3 Documents pending review", type: "task" },
          { id: "r2", title: "Orphaned entities detected", type: "alert" }
        ];
      } else {
        layoutWidgets = [
          { id: "w1", type: "equipment_status", title: "Assigned Equipment", grid_area: "span 2 / span 2" },
          { id: "w2", type: "learning_progress", title: "My Training", grid_area: "span 1 / span 1" },
          { id: "w3", type: "announcements", title: "Announcements", grid_area: "span 1 / span 2" },
          { id: "w4", type: "quick_actions", title: "Quick Actions", grid_area: "span 1 / span 1", settings: { actions: ["sop", "ticket", "copilot"] } }
        ];
        recs = [
          { id: "r1", title: "Review EAF Safety SOP", type: "sop" },
          { id: "r2", title: "Maintenance required for Pump A", type: "equipment" }
        ];
      }
      
      setProfile({
        user_id: "u-demo",
        role: role,
        preferences: { theme: "dark", accent_color: "#3182ce" },
        layout: { id: "tpl-1", name: `${role} Workspace`, widgets: layoutWidgets },
        ai_recommendations: recs
      });
      setLoading(false);
    }, 500);
  }, [role]);

  if (loading) return <div style={{ padding: '40px', color: '#a0aec0' }}>Loading Workspace...</div>;

  return (
    <div style={{ display: 'flex', height: '100%', background: '#111318', overflow: 'hidden' }}>
      
      {/* Main Workspace Area */}
      <div style={{ flex: 1, padding: '24px', overflowY: 'auto' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '32px' }}>
          <div>
            <h1 style={{ color: 'white', margin: '0 0 8px 0', fontSize: '32px' }}>Welcome back, Demo User</h1>
            <p style={{ color: '#a0aec0', margin: 0 }}>This is your personalized {profile.role} workspace.</p>
          </div>
          <div>
            <select 
              value={role} 
              onChange={(e) => setRole(e.target.value)}
              style={{ padding: '8px', background: '#2d3748', color: 'white', border: '1px solid #4a5568', borderRadius: '4px' }}
            >
              <option value="ENGINEER">View as Engineer</option>
              <option value="MASTER_EDITOR">View as Master Editor</option>
            </select>
          </div>
        </div>

        {/* Dynamic Widget Grid (CSS Grid simulation of Layout Manager) */}
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(3, 1fr)', 
          gridAutoRows: '200px', 
          gap: '24px' 
        }}>
          {profile.layout.widgets.map(widget => (
            <div key={widget.id} style={{ gridArea: widget.grid_area, transition: 'all 0.3s' }}>
              {WidgetRegistry.renderWidget(widget)}
            </div>
          ))}
        </div>
      </div>

      {/* Right Sidebar: AI Personalization */}
      <div style={{ width: '320px', background: '#1a1d24', borderLeft: '1px solid #2d3748', padding: '24px', overflowY: 'auto' }}>
        <h3 style={{ color: '#ecc94b', margin: '0 0 24px 0', display: 'flex', alignItems: 'center', gap: '8px' }}>
          ✨ AI Copilot
        </h3>
        
        <h4 style={{ color: '#a0aec0', textTransform: 'uppercase', fontSize: '12px', margin: '0 0 16px 0' }}>Recommended For You</h4>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          {profile.ai_recommendations.map(rec => (
            <div key={rec.id} style={{ padding: '16px', background: '#2d3748', borderRadius: '8px', cursor: 'pointer', border: '1px solid transparent' }} 
                 onMouseEnter={(e) => e.currentTarget.style.borderColor = profile.preferences.accent_color}
                 onMouseLeave={(e) => e.currentTarget.style.borderColor = 'transparent'}
            >
              <h5 style={{ color: 'white', margin: '0 0 4px 0', fontSize: '14px' }}>{rec.title}</h5>
              <span style={{ color: '#a0aec0', fontSize: '11px', textTransform: 'uppercase' }}>{rec.type}</span>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
}
