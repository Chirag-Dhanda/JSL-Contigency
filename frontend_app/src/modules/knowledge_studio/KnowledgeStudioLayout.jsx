import React, { useState } from 'react';
import { Routes, Route, Link, useLocation } from 'react-router-dom';
import EntityExplorer from './EntityExplorer';
import RelationshipExplorer from './RelationshipExplorer';
import MediaLibraryLayout from '../media_library/MediaLibraryLayout';
import ObjectDesigner from '../object_designer/ObjectDesigner';
import FlowBuilderLayout from '../manufacturing_builder/FlowBuilderLayout';
import ReviewCenterLayout from '../review_center/ReviewCenterLayout';
import PublishingCenter from '../publishing/PublishingCenter';
import ExplorerLayout from '../knowledge_explorer/ExplorerLayout';
import WorkspaceLayout from '../workspace/WorkspaceLayout';
import DashboardStudio from '../dashboard_studio/DashboardStudio';
import './KnowledgeStudio.css';

export default function KnowledgeStudioLayout() {
  const location = useLocation();

  return (
    <div className="ks-layout">
      <aside className="ks-sidebar">
        <div className="ks-brand">
          <h2>Enterprise</h2>
          <span>Knowledge Studio</span>
        </div>
        
        <nav className="ks-nav">
          <Link to="/studio" className={location.pathname === '/studio' ? 'active' : ''}>
            Dashboard
          </Link>
          <Link to="/studio/upload" className={location.pathname.includes('upload') ? 'active' : ''}>
            Knowledge Intake <span className="badge new">+</span>
          </Link>
          <Link to="/studio/entities" className={location.pathname.includes('entities') ? 'active' : ''}>
            Entity Explorer
          </Link>
          <Link to="/studio/relationships" className={location.pathname.includes('relationships') ? 'active' : ''}>
            Relationship Explorer
          </Link>
          <Link to="/studio/media" className={location.pathname.includes('media') ? 'active' : ''}>
            Media Library
          </Link>
          <Link to="/studio/publishing" className={location.pathname.includes('publishing') ? 'active' : ''}>
            Publishing Center
          </Link>
          <Link to="/studio/designer" className={location.pathname.includes('designer') ? 'active' : ''}>
            Object Designer
          </Link>
          <Link to="/studio/flow-builder" className={location.pathname.includes('flow-builder') ? 'active' : ''}>
            Flow Builder
          </Link>
          <Link to="/studio/review" className={location.pathname.includes('review') ? 'active' : ''}>
            Master Review Queue <span className="badge">1</span>
          </Link>
        </nav>
        
        <div className="ks-user-badge">
          <div className="avatar">ME</div>
          <div>
            <strong>Master Editor</strong>
            <small>Workspace Active</small>
          </div>
        </div>
      </aside>
      
      <main className="ks-main-content">
        <Routes>
          <Route path="/" element={<WorkspaceLayout />} />
          <Route path="/workspace" element={<WorkspaceLayout />} />
          <Route path="/dashboard-studio" element={<DashboardStudio />} />
          <Route path="/upload" element={<UploadWorkspace />} />
          <Route path="/entities" element={<EntityExplorer />} />
          <Route path="/relationships" element={<RelationshipExplorer />} />
          <Route path="/media" element={<MediaLibraryLayout />} />
          <Route path="/publishing" element={<PublishingCenter />} />
          <Route path="/designer" element={<ObjectDesigner />} />
          <Route path="/flow-builder" element={<FlowBuilderLayout />} />
          <Route path="/explore/:entityId" element={<ExplorerLayout />} />
          <Route path="/review" element={<ReviewCenterLayout />} />
          <Route path="/publishing" element={<PublishingCenter />} />
        </Routes>
      </main>
    </div>
  );
}

function StudioDashboard() {
  return (
    <div className="ks-dashboard">
      <header>
        <h1>Knowledge Studio Dashboard</h1>
        <p>Manage the Enterprise Knowledge Graph.</p>
      </header>
      
      <div className="ks-metrics-grid">
        <div className="ks-metric-card">
          <h3>Total Entities</h3>
          <div className="value">1,248</div>
        </div>
        <div className="ks-metric-card warning">
          <h3>Drafts Pending</h3>
          <div className="value">14</div>
        </div>
        <div className="ks-metric-card highlight">
          <h3>AI Suggestions</h3>
          <div className="value">3</div>
        </div>
      </div>
      
      <div className="ks-recent-activity">
        <h2>Recent Activity</h2>
        <ul className="activity-list">
          <li><strong>SOP-EAF-01</strong> was Published by admin.</li>
          <li><strong>furnace_schematic.pdf</strong> uploaded to Media Library.</li>
          <li><strong>AI generated</strong> a new lesson for AOD Operations.</li>
        </ul>
      </div>
    </div>
  );
}
