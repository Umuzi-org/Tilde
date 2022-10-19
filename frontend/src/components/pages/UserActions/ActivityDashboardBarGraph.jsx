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

export default function ActivityDashboardBarGraph({
  eventTypes,
  activityDayCounts,
}) {
  // will format data in index.js once redux wiring is done

  // get data set to look like:

  function prepareData(activityDayCounts, eventTypes) {
    const userActivityLogs = [];
    // need to group by date
    activityDayCounts.forEach((act) => {
      eventTypes.forEach((ev) => {
        if (ev.id === act.eventType) {
          const updated = {};
          updated.date = act.date;
          userActivityLogs.push(
            Object.assign(updated, { [ev.name]: act.total })
          );
        }
      });
    });
    console.log(userActivityLogs);
  }

  prepareData(activityDayCounts, eventTypes);

  const data = [
    {
      date: "2022-08-12",
      COMPETENCE_REVIEW_DONE: 6,
      CARD_MOVED_TO_REVIEW_FEEDBACK: 3,
      CARD_MOVED_TO_COMPLETE: 4,
    },
    {
      date: "2022-08-11",
      COMPETENCE_REVIEW_DONE: 2,
      PR_REVIEWED: 6,
      CARD_MOVED_TO_REVIEW_FEEDBACK: 3,
    },
    {
      date: "2022-08-10",
      CARD_MOVED_TO_COMPLETE: 5,
    },
  ];

  // draw a bar for each event type
  // check if the metric exists in the object before you draw

  return (
    <BarChart
      width={500}
      height={300}
      data={data}
      margin={{
        top: 5,
        right: 30,
        left: 20,
        bottom: 5,
      }}
    >
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="date" padding={{ left: 0, right: 0 }} />
      <Tooltip />
      <Legend />
      {eventTypes.map((eventType) => (
        <Bar
          dataKey={eventType.name}
          fill={
            eventType.name === "CARD_MOVED_TO_COMPLETE"
              ? eventTypeColors.CARD_MOVED_TO_COMPLETE
              : eventType.name === "CARD_MOVED_TO_REVIEW_FEEDBACK"
              ? eventTypeColors.CARD_MOVED_TO_REVIEW_FEEDBACK
              : eventType.name === "CARD_REVIEW_REQUEST_CANCELLED"
              ? eventTypeColors.CARD_REVIEW_REQUEST_CANCELLED
              : eventType.name === "CARD_REVIEW_REQUESTED"
              ? eventTypeColors.CARD_REVIEW_REQUESTED
              : eventType.name === "CARD_STARTED"
              ? eventTypeColors.CARD_STARTED
              : "blue"
          }
          name={eventType.name.toLowerCase().replaceAll("_", " ")}
        />
      ))}
    </BarChart>
  );
}
