import React from "react";
import { BarChart, Bar, XAxis } from "recharts";
// import data from "../../../stories/fixtures/ActivityDashBoardBargraphData.json";

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
      <XAxis dataKey="date" />

      <Bar
        dataKey="total"
        fill={eventTypeColors.PROJECT_CARDS_COMPLETED}
        name="Project cards completed"
      />
      <Bar
        dataKey="topicCardsCompleted"
        fill={eventTypeColors.TOPIC_CARDS_COMPLETED}
        name="Topic cards completed"
      />
      <Bar
        dataKey="reviewsCompleted"
        fill={eventTypeColors.REVIEWS_COMPLETED}
        name="Reviews completed"
      />
    </BarChart>
  );
}
