import React from "react";
import { BarChart, Bar, XAxis, Legend, Tooltip, CartesianGrid } from "recharts";

import { eventTypeColors } from "../../../colors";

export default function ActivityDashboardBarGraph({ eventList }) {
  // will format data in index.js once redux wiring is done
  const userActivityLogs = [];
  eventList.forEach((events) => {
    if (!userActivityLogs.some((date) => date.date === events.date)) {
      const userActivity = {
        date: events.date,
        events: [events],
      };
      userActivityLogs.push(userActivity);
    } else if (userActivityLogs.some((date) => date.date === events.date)) {
      const dateIndex = userActivityLogs.findIndex((date) => {
        return date.date === events.date;
      });
      userActivityLogs[dateIndex].events.push(events);
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
        key.events.map((item) => (
          <Bar
            dataKey={() => item.total}
            fill={
              item.eventType === 1
                ? eventTypeColors.COMPETENCE_REVIEW_DONE
                : item.eventType === 6
                ? eventTypeColors.CARD_MOVED_TO_COMPLETE
                : item.eventType === 5
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
