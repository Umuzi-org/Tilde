import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  Legend,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";

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
  console.log(data);
  return (
    // <ResponsiveContainer width="100%">
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
      {/* {console.log("hey", eventList[1].snapshot[0].total)}; */} */}
      <Bar
        dataKey={() => data[0].snapshot[0].total}
        fill={eventTypeColors.PROJECT_CARDS_COMPLETED}
        name="Project cards completed"
      />
      {/* <Bar
        dataKey="total"
        fill={eventTypeColors.TOPIC_CARDS_COMPLETED}
        name="Topic cards completed"
      />
      <Bar
        dataKey="total"
        fill={eventTypeColors.REVIEWS_COMPLETED}
        name="Reviews completed"
      /> */}
    </BarChart>
    // </ResponsiveContainer>
  );
}
