import React from "react";
import { BarChart, Bar, XAxis, Legend, Tooltip, CartesianGrid } from "recharts";

import { eventTypeColors } from "../../../colors";

export default function ActivityDashboardBarGraph({ eventList }) {
  // will format data in index.js once redux wiring is done
  const userActivityLogs = [];
  eventList.forEach((snapshot) => {
    if (!userActivityLogs.some((date) => date.date === snapshot.date)) {
      const activitySnapshot = {
        id: snapshot.id,
        date: snapshot.date,
        snapshot: [snapshot],
      };
      userActivityLogs.push(activitySnapshot);
    } else if (userActivityLogs.some((date) => date.date === snapshot.date)) {
      const dateIndex = userActivityLogs.findIndex((date) => {
        return date.date === snapshot.date;
      });
      userActivityLogs[dateIndex].snapshot.push(snapshot);
    }
  });

  return (
    <BarChart
      width={1000}
      height={300}
      data={userActivityLogs}
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

      {userActivityLogs.map((key) =>
        key.snapshot.map((item) => (
          <Bar
            dataKey={() => item.total}
            fill={
              item.event_type === 1
                ? eventTypeColors.COMPETENCE_REVIEW_DONE
                : item.event_type === 6
                ? eventTypeColors.CARD_MOVED_TO_COMPLETE
                : item.event_type === 5
                ? eventTypeColors.CARD_MOVED_TO_REVIEW_FEEDBACK
                : "white"
            }
            name="random name"
          />
        ))
      )}
    </BarChart>
  );
}
