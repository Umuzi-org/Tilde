import React from "react";
import {
  BarChart,
  Cell,
  Bar,
  XAxis,
  Legend,
  Tooltip,
  CartesianGrid,
} from "recharts";

import { eventTypeColors } from "../../../colors";

export default function ActivityDashboardBarGraph({ activityDayCounts }) {
  // will format data in index.js once redux wiring is done
  const userActivityLogs = [];
  activityDayCounts.forEach((events) => {
    if (!userActivityLogs.some((date) => date.date === events.date)) {
      const userActivity = {
        id: events.id,
        events,
      };
      userActivityLogs.push(userActivity);
    } else if (userActivityLogs.some((date) => date.date === events.date)) {
      const dateIndex = userActivityLogs.findIndex((date) => {
        return date.date === events.date;
      });
      userActivityLogs[dateIndex].events.push(events);
    }
  });

  const unique = Array.from(
    new Set(userActivityLogs.map((index) => index.events.total))
  );

  const activityLogValues = Object.values(
    userActivityLogs.reduce((acc, curr) => {
      const {
        events: { date, total },
      } = curr;
      acc[date] = acc[date] || { date };
      acc[date][total] = (acc[date][total] || 0) + 1;
      acc[date][total] = curr.events.total;
      return acc;
    }, {})
  );

  return (
    <BarChart
      width={1000}
      height={300}
      data={activityLogValues}
      margin={{
        top: 25,
        right: 30,
        left: 20,
        bottom: 25,
      }}
    >
      <CartesianGrid />
      <XAxis dataKey="date" />
      <Tooltip />
      <Legend />

      {unique.map((total) => (
        <>
          <Bar dataKey={total} name="name" />
        </>
      ))}
    </BarChart>
  );
}
