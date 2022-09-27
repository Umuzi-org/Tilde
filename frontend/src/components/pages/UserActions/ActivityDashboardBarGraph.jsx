import React from "react";
import { BarChart, Bar, XAxis, CartesianGrid, Tooltip, Legend } from "recharts";
import data from "../../../stories/fixtures/ActivityDashBoardBargraphData.json";

import { eventTypeColors } from "../../../colors";

export default function ActivityDashboardBarGraph() {
  return (
    <BarChart
      width={1000}
      height={300}
      data={data}
      margin={{
        top: 5,
        right: 30,
        left: 20,
        bottom: 5,
      }}
    >
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="date" />
      <Tooltip />
      <Legend />
      <Bar
        dataKey="projectCardsCompleted"
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
