// import React, { PureComponent } from 'react';
import React from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import UserDetailedStats from "../../../stories/fixtures/userDetailedStats.json";
const data = [
  {
    name: '0',
    cardsCompleted: UserDetailedStats.cardsInCompletedColumnAsAssignee,
    projectsCompleted: 14,
    incompleteCards: 100,
    incompleteProjects: 240,
    amt: 240,
  },
  {
    name: '3',
    cardsCompleted: 300,
    projectsCompleted: 45,
    incompleteCards: 70,
    incompleteProjects: 139,
    amt: 221,
  },
  {
    name: '6',
    cardsCompleted: 200,
    projectsCompleted: 80,
    incompleteCards: 50,
    incompleteProjects: 980,
    amt: 229,
  },
  {
    name: '9',
    cardsCompleted: 278,
    projectsCompleted: 122,
    incompleteCards: 30,
    incompleteProjects: 390,
    amt: 200,
  },
];
 
export default ({}) => {
  return (
    <div>
      <h1>All Data is shown overtime</h1>
        <LineChart
      width={1000}
      height={500}
      data={data}
      margin={{
        top: 5,
        right: 30,
        left: 100,
        bottom: 5
      }}
    >
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="name" />
      <YAxis />
      <Tooltip />
      <Legend />
      <Line
        type="monotone"
        dataKey="incompleteProjects"
        stroke="black"
        activeDot={{ r: 8 }}
      />
      <Line type="monotone" dataKey="cardsCompleted" stroke="green" />
      <Line type="monotone" dataKey="projectsCompleted" stroke="blue" />
      <Line type="monotone" dataKey="incompleteCards" stroke="orange" />
    </LineChart>
    </div>
  );
};
