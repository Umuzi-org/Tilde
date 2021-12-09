import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";
import { data } from "./CardDataStats";

data.map(
  (date) =>
    (date.timestamp = new Date(date.timestamp).toISOString().slice(0, 10))
);
export default () => {
  return (
    <div>
      <LineChart
        width={1000}
        height={500}
        data={data}
        margin={{
          top: 20,
          right: 30,
          left: 100,
          bottom: 5,
        }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="timestamp" interval="preserveEnd" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line
          type="monotone"
          dataKey="cardsTotalCount"
          stroke="black"
          activeDot={{ r: 8 }}
        />
        <Line type="monotone" dataKey="projectCardsTotalCount" stroke="green" />
        <Line
          type="monotone"
          dataKey="cardsInCompleteColumnTotalCount"
          stroke="blue"
        />
        <Line
          type="monotone"
          dataKey="projectCardsInCompleteColumnTotalCount"
          stroke="orange"
        />
      </LineChart>
    </div>
  );
};
