import React from 'react';
import { Doughnut } from 'react-chartjs-2';
import { Chart, ArcElement, Tooltip } from 'chart.js';
import './InclusivityGauge.css';

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';

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

Chart.register(ArcElement, Tooltip);

export default function InclusivityGauge({ value = 3 }) {
  const data = {
    datasets: [
      {
        data: [value, 5 - value],
        backgroundColor: [
          value <= 1 ? '#E53935' : 
          value <= 2 ? '#FFEB3B' : 
          value <= 3 ? '#4CAF50' : 
          value <= 4 ? '#03A9F4' : 
          '#3F51B5',
          '#E0E0E0' // remaining part
        ],
        borderWidth: 0,
        cutout: '70%',
        circumference: 180,
        rotation: 270
      }
    ]
  };

  const options = {
    responsive: true,
    cutout: '70%',
    plugins: {
      tooltip: { enabled: false },
    }
  };

  return (
    <div className="gauge-card">
      <Doughnut data={data} options={options} />
      <div className="gauge-value">{value}</div>
      <div className="gauge-label">Inclusivity Index</div>
    </div>
  );
}

