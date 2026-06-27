import React, { useState } from 'react';
import FieldEditor from './FieldEditor';
import LivePreview from './LivePreview';

export default function ObjectDesigner() {
  const [activeTab, setActiveTab] = useState('fields');
  const [fields, setFields] = useState([]);

  const addField = (fieldType) => {
    setFields([...fields, {
      field_id: `field_${Date.now()}`,
      display_name: `New ${fieldType} Field`,
      field_type: fieldType,
      validation: { required: false }
    }]);
  };

  return (
    <div className="ks-page" style={{ display: 'flex', gap: '20px', height: '100%' }}>
      {/* LEFT: Designer Tooling */}
      <div style={{ flex: 1, background: '#1a1d24', padding: '24px', borderRadius: '8px', overflowY: 'auto' }}>
        <header style={{ marginBottom: '24px' }}>
          <h1>Enterprise Object Designer</h1>
          <p>Visually build dynamic business objects without writing code.</p>
        </header>

        <div style={{ display: 'flex', gap: '16px', marginBottom: '24px' }}>
          <button 
            style={{ padding: '8px 16px', background: activeTab === 'fields' ? '#3182ce' : '#2d3748', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
            onClick={() => setActiveTab('fields')}
          >
            Field Designer
          </button>
          <button 
            style={{ padding: '8px 16px', background: activeTab === 'behavior' ? '#3182ce' : '#2d3748', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
            onClick={() => setActiveTab('behavior')}
          >
            AI & Behavior
          </button>
        </div>

        {activeTab === 'fields' && (
          <div>
            <div style={{ display: 'flex', gap: '8px', marginBottom: '24px', flexWrap: 'wrap' }}>
              <button onClick={() => addField('TEXT')} style={btnStyle}>+ Text</button>
              <button onClick={() => addField('NUMBER')} style={btnStyle}>+ Number</button>
              <button onClick={() => addField('DROPDOWN')} style={btnStyle}>+ Dropdown</button>
              <button onClick={() => addField('FILE')} style={btnStyle}>+ File</button>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              {fields.length === 0 ? (
                <div style={{ color: '#a0aec0', fontStyle: 'italic' }}>No fields added yet.</div>
              ) : (
                fields.map((f, i) => (
                  <FieldEditor key={i} field={f} />
                ))
              )}
            </div>
          </div>
        )}

        {activeTab === 'behavior' && (
          <div style={{ color: '#a0aec0' }}>
            <p><strong>AI Integration Rules</strong></p>
            <p>[Mock: Form for embedding policy, AI tags, and search priority]</p>
          </div>
        )}

      </div>

      {/* RIGHT: Live Preview */}
      <div style={{ flex: 1, background: '#1a1d24', padding: '24px', borderRadius: '8px', borderLeft: '1px solid #2d3748' }}>
        <LivePreview fields={fields} />
      </div>
    </div>
  );
}

const btnStyle = {
  background: '#4a5568', color: '#fff', border: '1px solid #718096', padding: '4px 12px', borderRadius: '4px', cursor: 'pointer', fontSize: '12px'
};
