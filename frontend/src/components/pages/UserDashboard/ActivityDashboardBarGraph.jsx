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

// import { cardColors } from "../../../colors";

const data = [
  {
    name: "Date",
    topicCardsCompleted: 4000,
    projectCardsCompleted: 2400,
    reviewsCompleted: 1000,
    amt: 2400,
  },
  {
    name: "Date",
    topicCardsCompleted: 3000,
    projectCardsCompleted: 1398,
    reviewsCompleted: 3000,
    amt: 2210,
  },
  {
    name: "Date",
    topicCardsCompleted: 2000,
    projectCardsCompleted: 9800,
    reviewsCompleted: 1040,
    amt: 2290,
  },
  {
    name: "Date",
    topicCardsCompleted: 2780,
    projectCardsCompleted: 3908,
    reviewsCompleted: 1100,
    amt: 2000,
  },
  {
    name: "Date",
    topicCardsCompleted: 1890,
    projectCardsCompleted: 4800,
    reviewsCompleted: 2100,
    amt: 2181,
  },
  {
    name: "Date",
    topicCardsCompleted: 2390,
    projectCardsCompleted: 3800,
    reviewsCompleted: 1050,
    amt: 2500,
  },
  {
    name: "Date",
    topicCardsCompleted: 3490,
    projectCardsCompleted: 4300,
    reviewsCompleted: 1001,
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
      <Bar
        dataKey="projectCardsCompleted"
        fill="#FF0000"
        name="Project Cards Completed"
      />
      <Bar
        dataKey="topicCardsCompleted"
        fill="#00FF00"
        name="Topic Cards Completed"
      />
      <Bar dataKey="reviewsCompleted" fill="#F6BE00" name="Reviews Completed" />
    </BarChart>
  );
}
