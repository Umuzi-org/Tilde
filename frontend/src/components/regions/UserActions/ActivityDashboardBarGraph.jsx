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

import { eventTypeColors } from "../../../colors";

const data = [
  {
    id: "date=2022-08-12&event_type=1&filter_by_actor_user=2&filter_by_effected_user=",
    date: "2022-08-12",
    topicCardsCompleted: 4000,
    projectCardsCompleted: 2400,
    reviewsCompleted: 1000,
    
  },
  {
    id: "date=2022-08-12&event_type=5&filter_by_actor_user=2&filter_by_effected_user=",
    date: "2022-08-12",
    topicCardsCompleted: 3000,
    projectCardsCompleted: 1398,
    reviewsCompleted: 3000,
    
  },
  {
    id: "date=2022-08-12&event_type=6&filter_by_actor_user=2&filter_by_effected_user=",
    date: "2022-08-12",
    topicCardsCompleted: 2780,
    projectCardsCompleted: 3908,
    reviewsCompleted: 1100,
    
  },
  {
    id: "date=2022-08-11&event_type=1&filter_by_actor_user=2&filter_by_effected_user=",
    date: "2022-08-11",
    topicCardsCompleted: 1890,
    projectCardsCompleted: 4800,
    reviewsCompleted: 2100,

  },
];

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
      <XAxis dataKey="name" />
      {/* <YAxis /> */}
      <Tooltip />
      <Legend />
      <Bar
        dataKey="projectCardsCompleted"
        fill={eventTypeColors.CARD_MOVED_TO_COMPLETE}
        date="Project Cards Completed"
      />
      <Bar
        dataKey="topicCardsCompleted"
        fill={eventTypeColors.CARD_MOVED_TO_REVIEW_FEEDBACK}
        date="Topic Cards Completed"
      />
      <Bar
        dataKey="reviewsCompleted"
        fill={eventTypeColors.CARD_STARTED}
        date="Reviews Completed"
      />
    </BarChart>
  );
}
