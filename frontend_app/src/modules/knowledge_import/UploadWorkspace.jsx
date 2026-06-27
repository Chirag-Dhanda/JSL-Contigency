import React, { useState } from 'react';
import './KnowledgeImport.css';

export default function UploadWorkspace() {
  const [files, setFiles] = useState([]);
  const [uploading, setUploading] = useState(false);

  const handleDrop = (e) => {
    e.preventDefault();
    const droppedFiles = Array.from(e.dataTransfer.files);
    setFiles([...files, ...droppedFiles]);
  };

  const simulateUpload = () => {
    setUploading(true);
    setTimeout(() => {
      setUploading(false);
      setFiles([]);
      alert("Files submitted to AI Knowledge Architect. Please check the Review Queue.");
    }, 2000);
  };

  return (
    <div className="ks-page" style={{ padding: '24px', display: 'flex', flexDirection: 'column', height: '100%' }}>
      <header style={{ marginBottom: '24px' }}>
        <h1 style={{ margin: '0 0 8px 0', color: '#fff' }}>Knowledge Import Workspace</h1>
        <p style={{ margin: 0, color: '#a0aec0' }}>Upload engineering drawings, SOPs, and manuals. The AI will automatically extract entities and relationships.</p>
      </header>

      <div 
        className="upload-dropzone" 
        onDragOver={(e) => e.preventDefault()} 
        onDrop={handleDrop}
        style={{
          border: '2px dashed #4a5568',
          borderRadius: '8px',
          padding: '64px',
          textAlign: 'center',
          backgroundColor: '#1a1d24',
          marginBottom: '24px',
          cursor: 'pointer'
        }}
      >
        <div style={{ fontSize: '48px', marginBottom: '16px' }}>📂</div>
        <h3 style={{ color: '#e2e8f0', margin: '0 0 8px 0' }}>Drag & Drop Enterprise Files Here</h3>
        <p style={{ color: '#718096', margin: 0 }}>Supports PDF, DOCX, XLSX, Images, and ZIP archives</p>
        <button style={{ marginTop: '24px', padding: '10px 20px', background: '#3182ce', color: 'white', border: 'none', borderRadius: '4px' }}>
          Browse Files
        </button>
      </div>

      {files.length > 0 && (
        <div className="upload-queue" style={{ flex: 1, backgroundColor: '#1a1d24', borderRadius: '8px', padding: '16px' }}>
          <h4 style={{ color: '#fff', margin: '0 0 16px 0' }}>Ready for Intake ({files.length})</h4>
          <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
            {files.map((f, i) => (
              <li key={i} style={{ display: 'flex', justifyContent: 'space-between', padding: '12px', borderBottom: '1px solid #2d3748', color: '#e2e8f0' }}>
                <span>📄 {f.name || `EAF_Manual_v2.pdf`}</span>
                <span style={{ color: '#a0aec0' }}>Pending</span>
              </li>
            ))}
          </ul>
          
          <button 
            onClick={simulateUpload} 
            disabled={uploading}
            style={{ marginTop: '24px', width: '100%', padding: '12px', background: uploading ? '#4a5568' : '#38a169', color: 'white', border: 'none', borderRadius: '4px', fontWeight: 'bold' }}
          >
            {uploading ? 'AI Architect is Processing...' : 'Start Knowledge Intake Pipeline'}
          </button>
        </div>
      )}
      
      {/* Mock state for demo if empty */}
      {files.length === 0 && (
        <div style={{ textAlign: 'center', marginTop: '20px' }}>
            <button onClick={() => setFiles([{name: "EAF_Safety_Procedures.pdf"}])} style={{ padding: '8px 16px', background: '#2d3748', color: '#a0aec0', border: '1px solid #4a5568', borderRadius: '4px', cursor: 'pointer' }}>
              Load Demo Document
            </button>
        </div>
      )}
    </div>
  );
}
