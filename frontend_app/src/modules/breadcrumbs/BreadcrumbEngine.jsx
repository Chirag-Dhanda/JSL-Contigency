import React from 'react';
import { Link } from 'react-router-dom';

export default function BreadcrumbEngine({ breadcrumbs }) {
  if (!breadcrumbs || breadcrumbs.length === 0) return null;

  return (
    <nav style={{ marginBottom: '16px', fontSize: '13px', color: '#a0aec0' }}>
      {breadcrumbs.map((crumb, index) => (
        <span key={crumb.id}>
          {index > 0 && <span style={{ margin: '0 8px' }}>/</span>}
          {index === breadcrumbs.length - 1 ? (
            <span style={{ color: '#fff', fontWeight: 'bold' }}>{crumb.name}</span>
          ) : (
            <Link 
              to={`/studio/explore/${crumb.id}`}
              style={{ color: '#63b3ed', textDecoration: 'none' }}
              className="breadcrumb-link"
            >
              {crumb.name}
            </Link>
          )}
        </span>
      ))}
    </nav>
  );
}
