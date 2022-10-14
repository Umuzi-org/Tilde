import { yellow } from "@material-ui/core/colors";
import { DataUsage } from "@material-ui/icons";
import React from "react";
import { BarChart, Bar, XAxis, Legend, Tooltip, CartesianGrid } from "recharts";

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
    new Set(userActivityLogs.map((i) => i.events.total))
  );

  const activityLogValues = Object.values(
    userActivityLogs.reduce((acc, curr) => {
      const {
        events: { date, total },
      } = curr;
      acc[date] = acc[date] || { date };
      acc[date][total] = (acc[date][total] || 0) + 1;
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

      {unique.map((tot) => (
        <Bar dataKey={tot} fill={"blue"} name="random name" />
      ))}
    </BarChart>
  );
}
