import React from 'react';

export default function LivePreview({ fields }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      <h2 style={{ borderBottom: '1px solid #2d3748', paddingBottom: '16px', marginTop: 0 }}>
        Live Runtime Preview
      </h2>
      <p style={{ color: '#a0aec0', fontSize: '14px', marginBottom: '24px' }}>
        This is exactly how the entity will render for end users once published to the Runtime Generator.
      </p>
      
      <div style={{ background: '#0b0c10', padding: '24px', borderRadius: '8px', flex: 1 }}>
        <form style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          {fields.map((f, i) => (
            <div key={i} style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              <label style={{ color: '#e2e8f0', fontSize: '14px', fontWeight: 'bold' }}>
                {f.display_name} {f.validation?.required && <span style={{ color: '#e53e3e' }}>*</span>}
              </label>
              
              {f.field_type === 'TEXT' && (
                <input type="text" placeholder={`Enter ${f.display_name.toLowerCase()}...`} style={previewInputStyle} />
              )}
              {f.field_type === 'NUMBER' && (
                <input type="number" placeholder="0" style={previewInputStyle} />
              )}
              {f.field_type === 'DROPDOWN' && (
                <select style={previewInputStyle}>
                  <option>Select an option...</option>
                </select>
              )}
              {f.field_type === 'FILE' && (
                <div style={{ ...previewInputStyle, borderStyle: 'dashed', textAlign: 'center', color: '#a0aec0', padding: '24px' }}>
                  Drop file to upload to Media Library
                </div>
              )}
            </div>
          ))}
          
          {fields.length > 0 && (
            <button type="button" style={{ marginTop: '16px', background: '#38a169', color: '#fff', border: 'none', padding: '12px', borderRadius: '4px', fontWeight: 'bold', cursor: 'not-allowed' }}>
              Save Entity
            </button>
          )}
        </form>
      </div>
    </div>
  );
}

const previewInputStyle = {
  background: '#1a1d24', border: '1px solid #4a5568', color: '#fff', padding: '10px', borderRadius: '6px', width: '100%'
};
