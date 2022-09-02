import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";
import { colors } from "../../../colors";

console.log("BIG", colors);

const data = [
  {
    name: "Date",
    C: 4000,
    RF: 2400,
    IR: 1000,
    amt: 2400,
  },
  {
    name: "Date",
    C: 3000,
    RF: 1398,
    IR: 3000,
    amt: 2210,
  },
  {
    name: "Date",
    C: 2000,
    RF: 9800,
    IR: 1040,
    amt: 2290,
  },
  {
    name: "Date",
    C: 2780,
    RF: 3908,
    IR: 1100,
    amt: 2000,
  },
  {
    name: "Date",
    C: 1890,
    RF: 4800,
    IR: 2100,
    amt: 2181,
  },
  {
    name: "Date",
    C: 2390,
    RF: 3800,
    IR: 1050,
    amt: 2500,
  },
  {
    name: "Date",
    C: 3490,
    RF: 4300,
    IR: 1001,
    amt: 2100,
  },
];

export default function ActivityDashboardBarGraph() {
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
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="name" />
      <YAxis />
      <Tooltip />
      <Legend />
      <Bar dataKey="RF" fill="#FF0000" />
      <Bar dataKey="C" fill="#00FF00" />
      <Bar dataKey="IR" fill="#FFFF00" />
    </BarChart>
  );
}
