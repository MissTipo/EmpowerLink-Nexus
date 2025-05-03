// src/components/Reports/ReportCard.jsx
import React from 'react';

export default function ReportCard({ report }) {
  return (
    <div className="p-4 bg-white rounded shadow">
      <h3 className="font-medium text-lg">{report.title}</h3>
      <p className="text-sm text-gray-600">{new Date(report.date).toLocaleDateString()}</p>
      <p className="mt-2 text-gray-700">{report.summary}</p>
      <button className="mt-4 px-3 py-1 bg-teal-600 text-white rounded">Read More</button>
    </div>
  );
}
