import React from "react";
import { BarChart, Bar, XAxis, Legend, Tooltip, CartesianGrid } from "recharts";

import { eventTypeColors } from "../../../colors";

export default function ActivityDashboardBarGraph({ eventList }) {
  // will format data in index.js once redux wiring is done
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
      {data.map((y) =>
        y.snapshot.map((z, i) => console.log("bddn", z.total, i))
      )}

      {data.map((key) =>
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
            name={item.event_type_name.toLowerCase().replaceAll(/_/gi, " ")}
          />
        ))
      )}
    </BarChart>
  );
}
