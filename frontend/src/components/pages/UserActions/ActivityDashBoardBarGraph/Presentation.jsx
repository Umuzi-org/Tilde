import { Typography } from "@material-ui/core";
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

export default function ActivityDashboardBarGraph({
  eventTypes,
  barGraphData,
  formatEventTypeName,
}) {
  return (
    <Typography>
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
          <XAxis dataKey="date" angle={-20} fontSize="70%" fontWeight="bold" />
          <YAxis />
          <Tooltip />
          <Legend align="center" />

          {eventTypes.map((eventType) => (
            <Bar
              dataKey={eventType.name}
              fill={eventType.color}
              name={formatEventTypeName(eventType.name)}
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
    </Typography>
  );
}
