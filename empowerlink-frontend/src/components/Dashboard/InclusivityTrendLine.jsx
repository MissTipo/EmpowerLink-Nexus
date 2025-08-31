import React from 'react';
import { Line } from 'react-chartjs-2';
import { useQuery } from '@apollo/client';
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
import { GET_INCLUSIVITY_TREND } from '../../graphql/queries';

// Register only what's needed:
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

function safeParseDate(s) {
  if (!s) return null;
  let t = s.replace(' ', 'T');                     // in case a space sneaks in
  t = t.replace(/(\.\d{3})\d+/, '$1');             // trim microseconds to milliseconds
  if (!/[zZ]|[+\-]\d{2}:\d{2}$/.test(t)) t += 'Z'; // add Z if no timezone
  const d = new Date(t);
  return Number.isNaN(d.getTime()) ? null : d;
}

export default function InclusivityTrendLine({ regionId = 1 }) {
  const { data, loading, error } = useQuery(GET_INCLUSIVITY_TREND, {
    variables: { regionId },
    fetchPolicy: 'network-only',
  });

  if (loading) return <div className="chart-card">Loading trend…</div>;
  if (error)   return <div className="chart-card">Error loading trend</div>;

  const trend = data?.getInclusivityTrend ?? [];
  const dates = trend.map(pt => safeParseDate(pt.timestamp));

  const labels = dates.map(d =>
    d ? d.toLocaleDateString([], { month: 'short', day: 'numeric' }) : '—'
  );

  // const labels = trend.map(pt =>
  //   new Date(pt.createdAt).toLocaleDateString([], { month: "short", day: "numeric" })
  // );
  const values = trend.map(pt => pt.value);

  const chartData = {
    labels,
    datasets: [
      {
        label: 'Inclusivity Index',
        data: values,
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
    plugins: {
      legend: { display: false },
      tooltip: { enabled: true },
    },
  };

  return (
    <div className="chart-card">
      <h3>Inclusivity Index Over Time</h3>
      <Line data={chartData} options={options} />
    </div>
  );
}

