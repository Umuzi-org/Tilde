import React from "react";
import { BarChart, Bar, XAxis, Legend, Tooltip, CartesianGrid } from "recharts";

import { eventTypeColors } from "../../../colors";

export default function ActivityDashboardBarGraph({
  eventTypes,
  activityDayCounts,
}) {
  const plantColorsToEventTypes = () => {
    const eventTypeNames = [];

    for (const eventName in eventTypes) {
      eventTypeNames.push(eventTypes[eventName].name);
    }

    const colors = [...Object.values(eventTypeColors)];
    const sortedEventTypeNames = eventTypeNames.sort();
    const keys = [...Object.keys(eventTypeColors)].sort();

    for (let i = 0; i < eventTypes.length; i++) {
      if (sortedEventTypeNames[i] === keys[i]) {
        eventTypes[i].color = colors[i];
      }
    }
  };

  plantColorsToEventTypes();

  const prepareDataForBarGraph = () => {
    const userActivityLogs = [];

    activityDayCounts.forEach((act) => {
      eventTypes.forEach((ev) => {
        if (ev.id === act.eventType) {
          if (
            !userActivityLogs.some(
              (userActivityLog) => userActivityLog.date === act.date
            )
          ) {
            const updated = {};
            updated.date = act.date;
            userActivityLogs.push(
              Object.assign(updated, { [ev.name]: act.total })
            );
          } else {
            const dateIndex = userActivityLogs.findIndex((userActivityLog) => {
              return userActivityLog.date === act.date;
            });
            Object.assign(userActivityLogs[dateIndex], {
              [ev.name]: act.total,
            });
          }
        }
      });
    });
    return userActivityLogs;
  };

  return (
    <div>
      <BarChart
        width={500}
        height={300}
        data={prepareDataForBarGraph()}
        margin={{
          top: 0,
          right: 0,
          left: 0,
          bottom: 0,
        }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="date" />
        <Tooltip />
        <Legend />
        {eventTypes.map((eventType) => (
          <Bar
            barSize={50}
            dataKey={eventType.name}
            fill={eventType.color}
            name={eventType.name.toLowerCase().replaceAll("_", " ")}
          />
        ))}
      </BarChart>
    </div>
  );
}
