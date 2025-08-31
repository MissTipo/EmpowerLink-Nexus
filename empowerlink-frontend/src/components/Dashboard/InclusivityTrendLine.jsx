import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import { useApolloClient } from '@apollo/client';
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
import { GET_INCLUSIVITY_INDEX } from '../../graphql/queries';

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

export default function InclusivityTrendLine({regionId = 1}, pollInterval = 60000) {
  const client = useApolloClient();
  const [history, setHistory] = useState([]);

  useEffect(() => {
    // helper to fetch one datapoint
    const fetchPoint = async () => {
      try {
        const { data } = await client.query({
          query: GET_INCLUSIVITY_INDEX,
          variables: { regionId },
          fetchPolicy: "network-only",
        });
        const timestamp = new Date();
        setHistory(h => [
          ...h,
          {
            time: timestamp.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
            value: data.computeInclusivityIndex.value,
          },
        ]);
      } catch (err) {
        console.error("failed to fetch index:", err);
      }
    };

    // initial fetch, then poll
    fetchPoint();
    const iv = setInterval(fetchPoint, pollInterval);
    return () => clearInterval(iv);
  }, [client, regionId, pollInterval]);

  // const { data, loading, error } = useQuery(GET_INCLUSIVITY_TREND, {
  //   variables: { regionId },
  //   fetchPolicy: 'network-only',
  // });
  //
  // if (loading) return <div className="chart-card">Loading trend…</div>;
  // if (error)   return <div className="chart-card">Error loading trend</div>;
  //
  // // data.getInclusivityTrend is an array of { month, value }
  // const trend = data.getInclusivityTrend;
  // const labels = trend.map((pt) => pt.month);
  // const values = trend.map((pt) => pt.value);


  const chartData = {
    labels: history.map((pt) => pt.time),
    datasets: [
      {
        label: 'Inclusivity Index',
        data: history.map((pt) => pt.value),
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

