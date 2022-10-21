import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  Legend,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
  YAxis,
} from "recharts";
import createStyles from "@material-ui/core/styles/createStyles";

import { eventTypeColors } from "../../../colors";

export default function ActivityDashboardBarGraph({
  eventTypes,
  activityDayCounts,
}) {
  const formatEventTypeName = (str) => str.toLowerCase().replaceAll("_", " ");

  const injectColorsToEventTypes = () => {
    const eventTypeNames = [];

    for (const eventName in eventTypes) {
      eventTypeNames.push(eventTypes[eventName].name);
    }

    const colors = [...Object.values(eventTypeColors)];
    const sortedEventTypeNames = eventTypeNames.sort();
    const evenTypeKeys = [...Object.keys(eventTypeColors)].sort();

    for (let i = 0; i < eventTypes.length; i++) {
      if (sortedEventTypeNames[i] === evenTypeKeys[i]) {
        eventTypes[i].color = colors[i];
      }
    }
  };

  injectColorsToEventTypes();

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
            const obj = {};
            obj.date = act.date;
            userActivityLogs.push(Object.assign(obj, { [ev.name]: act.total }));
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
      <ResponsiveContainer width={"100%"} height={300} min-width={300}>
        <BarChart
          width={730}
          height={350}
          data={prepareDataForBarGraph()}
          margin={{
            top: 50,
            right: 0,
            left: 0,
            bottom: 50,
          }}
          barCategoryGap={"20%"}
          barGap="20"
        >
          <CartesianGrid strokeDasharray="3 3" opacity={0.4} />
          <XAxis dataKey="date" angle={-20} fontSize="70%" fontWeight="bold" />
          <YAxis />
          <Tooltip filterNull cursor={false} />
          <Legend align="center" />

          {eventTypes.map((eventType) => (
            <Bar
              dataKey={eventType.name}
              fill={eventType.color}
              name={formatEventTypeName(eventType.name)}
            />
          ))}
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
