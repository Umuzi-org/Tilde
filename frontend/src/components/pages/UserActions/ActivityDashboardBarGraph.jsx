import React from "react";
import { BarChart, Bar, XAxis, Legend, Tooltip, CartesianGrid } from "recharts";

import { eventTypeColors } from "../../../colors";

export default function ActivityDashboardBarGraph({ eventList }) {
  return (
    <BarChart
      width={1000}
      height={300}
      data={eventList}
      margin={{
        top: 5,
        right: 30,
        left: 20,
        bottom: 5,
      }}
    >
      <CartesianGrid />
      <XAxis dataKey="date" />
      <Tooltip />
      <Legend />
      <Bar
        dataKey="total"
        fill={eventTypeColors.PROJECT_CARDS_COMPLETED}
        name="Project cards completed"
      />
      <Bar
        dataKey="total"
        fill={eventTypeColors.TOPIC_CARDS_COMPLETED}
        name="Topic cards completed"
      />
      <Bar
        dataKey="total"
        fill={eventTypeColors.REVIEWS_COMPLETED}
        name="Reviews completed"
      />
    </BarChart>
  );
}
