import React, { useEffect, useState } from 'react';
import { Doughnut } from 'react-chartjs-2';
import { Chart, ArcElement, Tooltip } from 'chart.js';
import { useLazyQuery } from '@apollo/client';
import { GET_INCLUSIVITY_INDEX, GET_TASK_STATUS } from '../../graphql/queries';
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
// import { Line } from 'react-chartjs-2';

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

Chart.register(ArcElement, Tooltip);

export default function InclusivityGauge({ regionId = 1 }) {
  // poll every 5 seconds (5000 ms) for the latest inclusivity index
  const [taskId, setTaskId] = useState(null);
  const [value, setValue] = useState(null);

  const [startCompute] = useLazyQuery(GET_INCLUSIVITY_INDEX, {
    variables: { regionId },
    fetchPolicy: "network-only",
    onCompleted: (data) => {
      setTaskId(data.computeInclusivityIndex.taskId);
    },
  });

  const [pollTaskStatus] = useLazyQuery(GET_TASK_STATUS, {
    fetchPolicy: "network-only",
    onCompleted: (data) => {
      if (data.getTaskStatus.status === "SUCCESS") {
        setValue(data.getTaskStatus.value);
      } else if (data.getTaskStatus.status === "FAILURE") {
        console.error("Task failed:", data.getTaskStatus.error);
      }
    },
  });

  useEffect(() => {
    startCompute();
  }, [startCompute, regionId]);

  useEffect(() => {
    if (!taskId) return;

    const interval = setInterval(() => {
      pollTaskStatus({ variables: { taskId } });
    }, 5000);

    return () => clearInterval(interval);
  }, [pollTaskStatus, taskId]);

  if (value === null) return <div className="gauge-card">Loading…</div>;

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

