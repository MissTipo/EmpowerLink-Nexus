import React from 'react';
import { Doughnut } from 'react-chartjs-2';
import { Chart, ArcElement, Tooltip } from 'chart.js';
import { useQuery, useSubscription } from '@apollo/client';
import { GET_INCLUSIVITY_INDEX, SUBSCRIBE_TO_INDEX } from '../../graphql/queries';
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

export default function InclusivityGauge({ regionId = 1 }) {
  // poll every 5 seconds (5000 ms) for the latest inclusivity index
  const { data, loading, error } = useQuery(GET_INCLUSIVITY_INDEX, {
    variables: { regionId },
    fetchPolicy: "network-only",
    pollInterval: 30 * 60 * 1000,
  });

  // Handle live updates via subscription
  // useSubscription(SUBSCRIBE_TO_INDEX, {
  //   variables: { regionId },
  //   onSubscriptionData: ({ subscriptionData, client }) => {
  //     const newValue = subscriptionData.data.indexUpdated.current;
  //     client.writeQuery({
  //       query: GET_INCLUSIVITY_INDEX,
  //       variables: { regionId },
  //       data: { computeInclusivityIndex: { value: newValue } },
  //     });
  //   },
  // });

  if (loading) return <div className="gauge-card">Loading…</div>;
  if (error) return <div className="gauge-card">Error!</div>;

  const value = data.computeInclusivityIndex.value;


  const chartData = {
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
      <Doughnut data={chartData} options={options} />
      <div className="gauge-value">{value}</div>
      <div className="gauge-label">Inclusivity Index</div>
    </div>
  );
}

