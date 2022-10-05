import React from "react";
import { BarChart, Bar, XAxis, Legend, Tooltip, CartesianGrid } from "recharts";

import { eventTypeColors } from "../../../colors";

export default function ActivityDashboardBarGraph({ eventList }) {
  const data = [];
  eventList.forEach((snapshot) => {
    if (!data.some((date) => date.date === snapshot.date)) {
      const activitySnapshot = {
        id: snapshot.id,
        date: snapshot.date,
        snapshot: [snapshot],
      };
      data.push(activitySnapshot);
    } else if (data.some((date) => date.date === snapshot.date)) {
      const dateIndex = data.findIndex((date) => {
        return date.date === snapshot.date;
      });
      data[dateIndex].snapshot.push(snapshot);
    }
  });

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
      <CartesianGrid />
      <XAxis dataKey="date" />
      <Tooltip />
      <Legend />

      {data.map((x, i) => (
        <Bar
          dataKey={() => x.snapshot[0].total}
          fill={eventTypeColors.PROJECT_CARDS_COMPLETED}
          name={() => x.snapshot[0].event_type_name}
        />
      ))}
    </BarChart>
  );
}
