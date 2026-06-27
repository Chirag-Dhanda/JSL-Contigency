import React, { useState, useEffect } from 'react';

export default function ReviewCenter() {
  const [jobs, setJobs] = useState([]);

  // Mock data for the demo
  useEffect(() => {
    setJobs([
      {
        id: "job-12345",
        filename: "EAF_Safety_Procedures.pdf",
        status: "IN_REVIEW",
        ai_summary: "Analyzed SOP document. Proposed 3 entities and 4 connections. Prepared 1 SAP mapping placeholders.",
        proposed_entities: [
          { type: "sop", name: "EAF Safety Procedures", confidence: 99 },
          { type: "equipment", name: "Electric Arc Furnace", confidence: 85 },
          { type: "sap_unresolved_mapping", name: "SAP Sync: Electric Arc Furnace", confidence: 100 }
        ],
        proposed_relationships: [
          { source: "EAF Safety Procedures", target: "Electric Arc Furnace", type: "REFERENCES_EQUIPMENT" }
        ]
      }
    ]);
  }, []);

  const handleApprove = (id) => {
    setJobs(jobs.filter(j => j.id !== id));
    alert("Approved! Entities committed to Knowledge Graph.");
  };

  return (
    <div className="ks-page" style={{ padding: '24px', display: 'flex', flexDirection: 'column', height: '100%' }}>
      <header style={{ marginBottom: '24px' }}>
        <h1 style={{ margin: '0 0 8px 0', color: '#fff' }}>Master Review Center</h1>
        <p style={{ margin: 0, color: '#a0aec0' }}>Review and approve AI-generated knowledge structures before they enter the live Enterprise Knowledge Graph.</p>
      </header>

      {jobs.length === 0 ? (
        <div style={{ padding: '40px', textAlign: 'center', color: '#a0aec0', background: '#1a1d24', borderRadius: '8px' }}>
          Queue is empty. All intake jobs have been processed.
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          {jobs.map(job => (
            <div key={job.id} style={{ background: '#1a1d24', border: '1px solid #2d3748', borderRadius: '8px', padding: '24px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '16px' }}>
                <div>
                  <h2 style={{ color: '#fff', margin: '0 0 8px 0', fontSize: '20px' }}>📄 {job.filename}</h2>
                  <p style={{ color: '#63b3ed', margin: 0, fontSize: '14px' }}>{job.ai_summary}</p>
                </div>
                <span style={{ background: '#c05621', color: 'white', padding: '4px 8px', borderRadius: '4px', fontSize: '12px', fontWeight: 'bold' }}>
                  AWAITING APPROVAL
                </span>
              </div>
              
              <div style={{ display: 'flex', gap: '24px', marginTop: '24px' }}>
                <div style={{ flex: 1 }}>
                  <h3 style={{ color: '#a0aec0', fontSize: '14px', borderBottom: '1px solid #2d3748', paddingBottom: '8px' }}>Proposed Entities ({job.proposed_entities.length})</h3>
                  <ul style={{ listStyle: 'none', padding: 0, margin: '12px 0' }}>
                    {job.proposed_entities.map((e, i) => (
                      <li key={i} style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 0', color: '#e2e8f0', fontSize: '14px' }}>
                        <span>
                          <span style={{ color: '#718096', marginRight: '8px' }}>[{e.type}]</span>
                          {e.name}
                        </span>
                        <span style={{ color: '#48bb78' }}>{e.confidence}%</span>
                      </li>
                    ))}
                  </ul>
                </div>
                
                <div style={{ flex: 1 }}>
                  <h3 style={{ color: '#a0aec0', fontSize: '14px', borderBottom: '1px solid #2d3748', paddingBottom: '8px' }}>Proposed Graph Edges ({job.proposed_relationships.length})</h3>
                  <ul style={{ listStyle: 'none', padding: 0, margin: '12px 0' }}>
                    {job.proposed_relationships.map((r, i) => (
                      <li key={i} style={{ padding: '8px 0', color: '#e2e8f0', fontSize: '13px' }}>
                        <span style={{ color: '#63b3ed' }}>{r.source}</span> <br/>
                        <span style={{ color: '#a0aec0', fontSize: '11px' }}>└─ [{r.type}] ─→</span> <span style={{ color: '#f6ad55' }}>{r.target}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
              
              <div style={{ marginTop: '24px', paddingTop: '16px', borderTop: '1px solid #2d3748', display: 'flex', justifyContent: 'flex-end', gap: '12px' }}>
                <button style={{ padding: '8px 16px', background: 'transparent', color: '#fc8181', border: '1px solid #fc8181', borderRadius: '4px', cursor: 'pointer' }}>Reject</button>
                <button onClick={() => handleApprove(job.id)} style={{ padding: '8px 16px', background: '#38a169', color: 'white', border: 'none', borderRadius: '4px', fontWeight: 'bold', cursor: 'pointer' }}>Approve & Publish</button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
