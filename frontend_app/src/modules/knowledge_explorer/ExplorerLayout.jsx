import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import SmartEntityPage from './SmartEntityPage';

export default function ExplorerLayout() {
  const { entityId } = useParams();
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);

  // Mocking the API call to the Discovery Engine
  useEffect(() => {
    setLoading(true);
    
    // In a real app, this would be: 
    // fetch(`/api/discovery/${entityId}`).then(res => res.json()).then(data => setProfile(data))
    
    // Mock Data for Demo Purposes based on Entity ID pattern
    setTimeout(() => {
      let type = "department";
      let name = "Enterprise Domain";
      if (entityId.startsWith("ent-")) name = "Electric Arc Furnace";
      if (entityId.startsWith("sop-")) { type = "sop"; name = "EAF Safety Protocol"; }
      
      const mockProfile = {
        entity: {
          id: entityId,
          name: `${name} (${entityId.substring(0,6)})`,
          type: type,
          attributes: { description: "This is a dynamically discovered entity profile." }
        },
        breadcrumbs: [
          { id: "home", name: "Enterprise Home" },
          { id: "plant-1", name: "Jajpur Plant" },
          { id: entityId, name: name }
        ],
        related_objects: {
          parents: [{ id: "plant-1", name: "Jajpur Plant", type: "plant", relationship: "BELONGS_TO" }],
          children: [{ id: "ent-2", name: "Control Room", type: "equipment", relationship: "BELONGS_TO" }],
          equipment: [{ id: "eq-1", name: "Primary Transformer", type: "equipment", relationship: "USES_EQUIPMENT" }],
          sops: [{ id: "sop-1", name: "High Voltage Protocol", type: "sop", relationship: "REQUIRES_SOP" }],
          lessons: [{ id: "less-1", name: "Arc Safety 101", type: "lesson", relationship: "REQUIRES_LESSON" }],
          other: []
        },
        recommendations: [
          { id: "rec-1", name: "EAF Process Flow", type: "workflow" },
          { id: "rec-2", name: "Recent Maintenance Ticket", type: "ticket" }
        ]
      };
      
      setProfile(mockProfile);
      setLoading(false);
    }, 500);

  }, [entityId]);

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%', color: '#a0aec0' }}>
        <h2>Discovering Context...</h2>
      </div>
    );
  }

  return (
    <div className="ks-page" style={{ display: 'flex', flexDirection: 'column', height: '100%', background: '#111318' }}>
      <SmartEntityPage profile={profile} />
    </div>
  );
}
