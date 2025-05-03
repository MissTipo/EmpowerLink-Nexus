import React from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';
import './TrendChart.css';

export default function TrendChart({ data }) {
  return (
    <div className="trend-chart">
      <h3 className="chart-title">Inclusivity Trend</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid stroke="#2A2A2A" />
          <XAxis dataKey="month" stroke="#E1E8EB" />
          <YAxis stroke="#E1E8EB" />
          <Tooltip contentStyle={{ backgroundColor: '#121917', border: 'none' }} />
          <Line type="monotone" dataKey="value" stroke="#FFD54F" strokeWidth={3} dot={{ r: 4, stroke: '#FFD54F', fill: '#121917' }} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

