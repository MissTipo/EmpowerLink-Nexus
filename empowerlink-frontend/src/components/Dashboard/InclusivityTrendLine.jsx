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
import { GET_INCLUSIVITY_INDEX, GET_TASK_STATUS } from '../../graphql/queries';

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

export default function InclusivityTrendLine({regionId = 1, pollInterval = 60000}) {
  const client = useApolloClient();
  const [history, setHistory] = useState([]);

  useEffect(() => {
    let pollTimer;
    let statusTimeout
    let isMounted = true;

    const fetchPoint = async () => {
      try {
        // Kick off computation -> returns taskId
        const { data } = await client.query({
          query: GET_INCLUSIVITY_INDEX,
          variables: { regionId },
          fetchPolicy: "network-only",
        });

        const taskId = data.computeInclusivityIndex.taskId;
        if (!taskId) {
          console.error("No taskId returned from computeInclusivityIndex");
          return;
        }

        // Poll task status until value is ready
        const checkStatus = async () => {
          if (!isMounted) return;
          const res = await client.query({
            query: GET_TASK_STATUS,
            variables: { taskId },
            fetchPolicy: 'network-only',
          });
          const task = res.data.getTaskStatus;
          if (task.status === "SUCCESS" && task.value !== null) {
            const timestamp = new Date();
            setHistory(h => [
              ...h.slice(-49),
              {
                time: timestamp.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
                value: task.value,
              },
            ]);
          } else if (task.status === "PENDING" || task.status === "STARTED") {
            // keep polling until it's done
            statusTimeout = setTimeout(checkStatus, 2000);
          } else if (task.status === "FAILURE") {
            console.error("Task failed:", task.error);
          }
        };
        checkStatus();
      } catch (err) {
        console.error("failed to fetch index:", err);
      }
    };

    // initial fetch, then schedule periodic re-computation
    fetchPoint();
    pollTimer = setInterval(fetchPoint, pollInterval);
    return () => {
      isMounted = false;
      clearTimeout(statusTimeout);
      clearInterval(pollTimer);
    };
  }, [client, regionId, pollInterval]);

  
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
