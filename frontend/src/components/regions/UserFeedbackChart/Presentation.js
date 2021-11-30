// import React, { PureComponent } from 'react';
import React from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const data = [
  {
    name: 'Cards completed',
    uv: 400,
    pv: 240,
    amt: 240,
  },
  {
    name: 'Projects completed',
    uv: 300,
    pv: 139,
    amt: 221,
  },
  {
    name: 'Incomplete cards',
    uv: 200,
    pv: 980,
    amt: 229,
  },
  {
    name: 'Incomplete project cards',
    uv: 278,
    pv: 390,
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
        dataKey="pv"
        stroke="#8884d8"
        activeDot={{ r: 8 }}
      />
      <Line type="monotone" dataKey="uv" stroke="#82ca9d" />
    </LineChart>
    </div>
  );
};
