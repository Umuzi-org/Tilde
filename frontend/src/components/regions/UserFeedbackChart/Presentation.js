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
const colorArr = ["orange", "green", "black", "blue"];
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
          stroke={colorArr[2]}
          activeDot={{ r: 8 }}
        />
        <Line type="monotone" dataKey="projectCardsTotalCount" stroke={colorArr[1]} />
        <Line
          type="monotone"
          dataKey="cardsInCompleteColumnTotalCount"
          stroke={colorArr[3]}
        />
        <Line
          type="monotone"
          dataKey="projectCardsInCompleteColumnTotalCount"
          stroke={colorArr[0]}
        />
      </LineChart>
    </div>
  );
};
