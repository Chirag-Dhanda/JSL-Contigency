import React, { useState } from 'react';
import './MediaLibrary.css';
import AssetPreviewModal from './AssetPreviewModal';

export default function MediaLibraryLayout() {
  const [activeTab, setActiveTab] = useState('all');
  const [selectedAsset, setSelectedAsset] = useState(null);

  // Mock Assets
  const [assets, setAssets] = useState([
    { id: '1', filename: 'AOD_Furnace_Diagram.pdf', type: 'PDF', tags: ['Equipment', 'Drawing'], ai_keywords: ['AOD', 'dimensions'], uploaded_at: '2026-06-25', owner: 'system' },
    { id: '2', filename: 'Safety_Briefing_Q3.mp4', type: 'Video', tags: ['Safety', 'Training'], ai_keywords: ['PPE', 'hazards'], uploaded_at: '2026-06-20', owner: 'system' },
    { id: '3', filename: 'Scrap_Yard_Layout.dwg', type: 'CAD', tags: ['Blueprint', 'Plant'], ai_keywords: ['layout', 'zones'], uploaded_at: '2026-06-18', owner: 'system' },
    { id: '4', filename: 'Pump_Maintenance.docx', type: 'Document', tags: ['SOP', 'Maintenance'], ai_keywords: ['pump', 'seal', 'replacement'], uploaded_at: '2026-06-27', owner: 'system' },
    { id: '5', filename: 'Equipment_Damage_Report.jpg', type: 'Image', tags: ['Incident', 'Quality'], ai_keywords: ['crack', 'casing'], uploaded_at: '2026-06-26', owner: 'system' },
  ]);

  const filteredAssets = activeTab === 'all' ? assets : assets.filter(a => a.type.toLowerCase() === activeTab);

  const getIconForType = (type) => {
    switch(type) {
      case 'PDF': return '📄';
      case 'Video': return '🎥';
      case 'CAD': return '📐';
      case 'Image': return '🖼️';
      case 'Document': return '📝';
      default: return '📁';
    }
  };

  return (
    <div className="ks-page" style={{ display: 'flex', flexDirection: 'column', height: '100%', padding: '24px' }}>
      <header style={{ marginBottom: '24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h1 style={{ margin: '0 0 8px 0', color: '#fff' }}>Digital Asset Library</h1>
          <p style={{ margin: 0, color: '#a0aec0' }}>Manage, search, and version all enterprise media. Assets are automatically tagged by AI.</p>
        </div>
        <div>
          <button style={{ background: '#3182ce', color: 'white', padding: '10px 20px', border: 'none', borderRadius: '4px', fontWeight: 'bold', cursor: 'pointer' }}>
            Upload Asset
          </button>
        </div>
      </header>

      <div style={{ display: 'flex', gap: '24px', flex: 1, overflow: 'hidden' }}>
        {/* Sidebar Filters */}
        <div style={{ width: '250px', background: '#1a1d24', borderRadius: '8px', border: '1px solid #2d3748', padding: '16px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
          <h3 style={{ color: '#fff', fontSize: '14px', marginBottom: '12px', textTransform: 'uppercase' }}>Media Types</h3>
          {['all', 'pdf', 'image', 'video', 'document', 'cad'].map(tab => (
            <button 
              key={tab}
              onClick={() => setActiveTab(tab)}
              style={{
                textAlign: 'left',
                padding: '8px 12px',
                background: activeTab === tab ? '#2b6cb0' : 'transparent',
                color: activeTab === tab ? '#fff' : '#a0aec0',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer',
                textTransform: 'capitalize'
              }}
            >
              {tab === 'all' ? 'All Assets' : tab}
            </button>
          ))}
          
          <h3 style={{ color: '#fff', fontSize: '14px', marginTop: '24px', marginBottom: '12px', textTransform: 'uppercase' }}>AI Tags</h3>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
            {['Safety', 'Equipment', 'SOP', 'Training', 'Incident'].map(tag => (
              <span key={tag} style={{ background: '#2d3748', color: '#e2e8f0', padding: '4px 8px', borderRadius: '4px', fontSize: '12px', cursor: 'pointer' }}>
                {tag}
              </span>
            ))}
          </div>
        </div>

        {/* Media Grid */}
        <div style={{ flex: 1, overflowY: 'auto' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '16px' }}>
            <input 
              type="text" 
              placeholder="Search assets, metadata, AI keywords..." 
              style={{ width: '400px', padding: '10px', background: '#1a1d24', border: '1px solid #4a5568', borderRadius: '4px', color: '#fff' }}
            />
            <span style={{ color: '#a0aec0', alignSelf: 'center' }}>{filteredAssets.length} Assets Found</span>
          </div>

          <div className="media-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: '20px' }}>
            {filteredAssets.map(asset => (
              <div 
                key={asset.id} 
                className="media-card"
                onClick={() => setSelectedAsset(asset)}
                style={{ background: '#1a1d24', border: '1px solid #2d3748', borderRadius: '8px', overflow: 'hidden', cursor: 'pointer', transition: 'all 0.2s' }}
              >
                <div style={{ height: '140px', background: '#2d3748', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '48px' }}>
                  {getIconForType(asset.type)}
                </div>
                <div style={{ padding: '12px' }}>
                  <h4 style={{ color: '#e2e8f0', margin: '0 0 4px 0', fontSize: '14px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                    {asset.filename}
                  </h4>
                  <p style={{ color: '#a0aec0', fontSize: '12px', margin: 0 }}>{asset.type} • {asset.uploaded_at}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {selectedAsset && (
        <AssetPreviewModal 
          asset={selectedAsset} 
          icon={getIconForType(selectedAsset.type)}
          onClose={() => setSelectedAsset(null)} 
        />
      )}
    </div>
  );
}
