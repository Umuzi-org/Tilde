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
  Cell,
} from "recharts";
import Typography from "@material-ui/core/Typography";

import { replaceUnderscoresWithSpace } from "./utils";

export default function ActivityDashboardBarGraph({
  eventTypes,
  barGraphData,
}) {
  return (
    <React.Fragment>
      <Typography variant="h6" component="h2">
        Activity Log Bar Graph
      </Typography>
      <ResponsiveContainer width={"100%"} height={300} min-width={500}>
        <BarChart
          width={730}
          height={350}
          data={barGraphData}
          margin={{
            top: 50,
            right: 0,
            left: 0,
            bottom: 50,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" opacity={0.4} />
          <XAxis dataKey="date" fontSize="70%" fontWeight="bold" />
          <YAxis allowDecimals={false} />
          <Tooltip />
          <Legend align="center" />

          {eventTypes.map((eventType) => (
            <Bar
              key={eventType.id}
              dataKey={eventType.name}
              fill={eventType.color}
              name={replaceUnderscoresWithSpace(eventType.name)}
            >
              {barGraphData.map((entry, index) => {
                return (
                  <Cell
                    display={entry[eventType.name] ? "" : "none"}
                    key={index}
                  />
                );
              })}{" "}
            </Bar>
          ))}
        </BarChart>
      </ResponsiveContainer>
    </React.Fragment>
  );
}
