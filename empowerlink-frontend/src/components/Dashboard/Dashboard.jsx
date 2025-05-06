import React from 'react';
import './Dashboard.css';
import Hero from './Hero';
import MapChart from './MapChartNew';
import InclusivityGauge from './InclusivityGauge';
import InclusivityTrendLine from './InclusivityTrendLine';
import ResourceMatches from './ResourceMatches';
import empowerDesign from '../../assets/empower2.avif';

export default function Dashboard() {
  return (
    <div className="dashboard-page">
      <Hero
        title="EmpowerLink Nexus"
        subtitle="Inclusive Empowerment & Resource Network"
      >
        <MapChart />
      </Hero>

      <div className="dashboard-stats">
        <InclusivityGauge />
        <InclusivityTrendLine />
        <ResourceMatches />
      </div>
      <div className="dashboard-bottom">
        <div className="bottom-card">
          <img src={empowerDesign} alt="Community Impact" style={{ maxWidth: '100%', borderRadius: '8px' }} />
        </div>

        <div className="bottom-card">
          <h3>Community Impact Reports</h3>
          <p>Summary of recent activities and initiatives. Click below to view detailed reports.</p>
          <a href="/impact-reports" className="btn">View Reports</a>
        </div>

        <div className="bottom-card">
          <h3>Feedback</h3>
          <p>See what the community is saying and share your thoughts.</p>
          <a href="/feedback" className="btn">Give Feedback</a>
        </div>
      </div>
    </div>
  );
}

