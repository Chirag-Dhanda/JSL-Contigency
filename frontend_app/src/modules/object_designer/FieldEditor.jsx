import React from 'react';

export default function FieldEditor({ field }) {
  return (
    <div style={{ background: '#2d3748', padding: '16px', borderRadius: '6px', border: '1px solid #4a5568' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '12px' }}>
        <h4 style={{ margin: 0, color: '#e2e8f0' }}>{field.display_name}</h4>
        <span style={{ fontSize: '11px', background: '#3182ce', color: '#fff', padding: '2px 8px', borderRadius: '12px' }}>
          {field.field_type}
        </span>
      </div>
      
      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
        <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
          <label style={{ fontSize: '12px', color: '#a0aec0', width: '80px' }}>Field ID:</label>
          <input type="text" defaultValue={field.field_id} style={inputStyle} readOnly />
        </div>
        
        <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
          <label style={{ fontSize: '12px', color: '#a0aec0', width: '80px' }}>Required:</label>
          <input type="checkbox" defaultChecked={field.validation?.required} />
        </div>
      </div>
    </div>
  );
}

const inputStyle = {
  background: '#1a202c', border: '1px solid #4a5568', color: '#fff', padding: '4px 8px', borderRadius: '4px', flex: 1
};
