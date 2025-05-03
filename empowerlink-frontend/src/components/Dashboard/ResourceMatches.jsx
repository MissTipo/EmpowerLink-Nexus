import React from 'react';
import './DashboardCharts.css';

export default function ResourceMatchesProgress() {
  const resources = [
    { name: 'Healthcare', value: 80 },
    { name: 'Legal', value: 65 },
    { name: 'Social Protection', value: 90 },
    { name: 'Economic Empowerment', value: 75 },
    { name: 'Education', value: 85 },
  ];

  return (
    <div className="chart-card">
      <h3>Resource Matches</h3>
      {resources.map((res, index) => (
        <div key={index} style={{ marginBottom: '0.75rem' }}>
          <span style={{ fontSize: '0.95rem' }}>{res.name}</span>
          <div style={{
            backgroundColor: '#e0f7fa',
            borderRadius: '20px',
            overflow: 'hidden',
            height: '16px',
            marginTop: '4px'
          }}>
            <div style={{
              width: `${res.value}%`,
              backgroundColor: '#03a9f4',
              height: '100%',
              borderRadius: '20px'
            }}></div>
          </div>
        </div>
      ))}
    </div>
  );
}

