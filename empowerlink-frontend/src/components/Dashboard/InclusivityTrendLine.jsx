import React from 'react';
import { Line } from 'react-chartjs-2';
import './DashboardCharts.css';

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

// Register only what you need:
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

export default function InclusivityTrendLine() {
  const data = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
    datasets: [
      {
        label: 'Inclusivity Index',
        data: [2.5, 3, 3.2, 3.6, 3.8],
        borderColor: '#03a9f4',
        backgroundColor: 'rgba(3, 169, 244, 0.2)',
        tension: 0.4,
        fill: true,
      },
    ],
  };

  const options = {
    responsive: true,
    scales: {
      y: { min: 0, max: 5 },
    },
  };

  return (
    <div className="chart-card">
      <h3>Inclusivity Index Over Time</h3>
      <Line data={data} options={options} />
    </div>
  );
}

