import React from 'react';
import './ReportsPage.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faFileAlt } from '@fortawesome/free-solid-svg-icons';

export default function ReportsPage() {
  const reports = [
    { id: 1, title: "Quarter 1 Inclusion Index", date: "2025-03-30", status: "Published" },
    { id: 2, title: "Annual Community Feedback", date: "2025-02-18", status: "Draft" },
    { id: 3, title: "Volunteer Allocation Report", date: "2025-01-10", status: "Published" },
  ];

  return (
    <div className="reports-page">
      <div className="page-title">
        <h1>Reports</h1>
      </div>

      <div className="reports-list">
        {reports.map((report) => (
          <div className="report-card" key={report.id}>
            <FontAwesomeIcon icon={faFileAlt} className="report-icon" />
            <div className="report-details">
              <h2>{report.title}</h2>
              <p>{report.date}</p>
            </div>
            <span className={`status-badge ${report.status.toLowerCase()}`}>
              {report.status}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

