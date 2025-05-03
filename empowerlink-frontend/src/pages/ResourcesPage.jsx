import React from 'react';
import './ResourcesPage.css';

export default function ResourcesPage() {
  return (
    <div className="resources-page">
      <div className="hero-banner">
        <img src="/srcassets/empower_design.png" alt="Empower Design" />
        <h1>Available Resources</h1>
      </div>

      <div className="resource-controls">
        <input
          type="text"
          placeholder="Search resources..."
          className="resource-search"
        />
        <button className="filter-btn">Filter</button>
      </div>

      <div className="resource-grid">
        <div className="resource-card">Resource 1</div>
        <div className="resource-card">Resource 2</div>
        <div className="resource-card">Resource 3</div>
        <div className="resource-card">Resource 4</div>
        {/* Repeat as needed */}
      </div>
    </div>
  );
}

