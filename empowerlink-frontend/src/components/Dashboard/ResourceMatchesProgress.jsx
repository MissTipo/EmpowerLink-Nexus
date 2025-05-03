// src/components/Dashboard/ResourceMatches.jsx
import React from 'react';

const dummyResources = [
  { id: 1, name: 'Jane Doe', role: 'Mentor' },
  { id: 2, name: 'Dr. Smith', role: 'Legal Aid' },
  { id: 3, name: 'Alex Johnson', role: 'Mentor' },
];

export default function ResourceMatches() {
  return (
    <div className="space-y-4">
      {dummyResources.map(r => (
        <div key={r.id} className="p-4 bg-white rounded shadow flex justify-between items-center">
          <div>
            <p className="font-medium">{r.name}</p>
            <p className="text-sm text-gray-500">{r.role}</p>
          </div>
          <button className="px-3 py-1 bg-red-500 text-white rounded">Cancel</button>
        </div>
      ))}
    </div>
  );
}
