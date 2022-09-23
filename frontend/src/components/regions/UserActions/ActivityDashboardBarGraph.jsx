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

const RED = eventTypeColors.CARD_MOVED_TO_REVIEW_FEEDBACK;
const GREEN = eventTypeColors.CARD_STARTED;
const YELLOW = eventTypeColors.CARD_MOVED_TO_COMPLETE;

export default function ActivityDashboardBarGraph({ activityLogDayCounts }) {
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
      <XAxis dataKey="date" />
      <YAxis />
      <Tooltip />
      <Legend />
      <Bar dataKey="eventType" fill={RED} name="Project Cards Completed" />
      <Bar dataKey="eventType" fill={GREEN} name="Topic Cards Completed" />
      <Bar dataKey="eventType" fill={YELLOW} name="Reviews Completed" />
    </BarChart>
  );
}
