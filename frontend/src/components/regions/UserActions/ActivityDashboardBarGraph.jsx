import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";

export default function ActivityDashboardBarGraph({ activityLogDayCounts }) {
  // console.log("TESST", activityLogDayCounts);
  return (
    <BarChart
      width={1000}
      height={300}
      data={activityLogDayCounts}
      margin={{
        top: 5,
        right: 30,
        left: 20,
        bottom: 5,
      }}
    >
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="name" />
      <YAxis />
      <Tooltip />
      <Legend />
      <Bar
        dataKey="projectCardsCompleted"
        fill="#FF0000"
        name="Project Cards Completed"
      />
      <Bar
        dataKey="topicCardsCompleted"
        fill="#00FF00"
        name="Topic Cards Completed"
      />
      <Bar dataKey="reviewsCompleted" fill="#F6BE00" name="Reviews Completed" />
    </BarChart>
  );
}
