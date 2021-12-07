// import React, { PureComponent } from 'react';
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

const data = [
  {
    user: 1,
    timestamp: "2019-08-09T13:49:31Z",
    cardsTotalCount: 32,
    projectCardsTotalCount: 25,
    cardsInCompleteColumnTotalCount: 10,
    projectCardsInCompleteColumnTotalCount: 7,
  },
  {
    user: 1,
    timestamp: "2019-08-10T13:49:31Z",
    cardsTotalCount: 35,
    projectCardsTotalCount: 21,
    cardsInCompleteColumnTotalCount: 14,
    projectCardsInCompleteColumnTotalCount: 11,
  },
  {
    user: 1,
    timestamp: "2019-08-11T13:49:31Z",
    cardsTotalCount: 39,
    projectCardsTotalCount: 26,
    cardsInCompleteColumnTotalCount: 17,
    projectCardsInCompleteColumnTotalCount: 14,
  },
  {
    user: 1,
    timestamp: "2019-08-12T13:49:31Z",
    cardsTotalCount: 44,
    projectCardsTotalCount: 30,
    cardsInCompleteColumnTotalCount: 22,
    projectCardsInCompleteColumnTotalCount: 18,
  },
  {
    user: 1,
    timestamp: "2019-08-13T13:49:31Z",
    cardsTotalCount: 47,
    projectCardsTotalCount: 35,
    cardsInCompleteColumnTotalCount: 27,
    projectCardsInCompleteColumnTotalCount: 24,
  },
  {
    user: 1,
    timestamp: "2019-08-14T13:49:31Z",
    cardsTotalCount: 50,
    projectCardsTotalCount: 41,
    cardsInCompleteColumnTotalCount: 32,
    projectCardsInCompleteColumnTotalCount: 29,
  },
  {
    user: 2,
    timestamp: "2019-08-15T13:49:31Z",
    cardsTotalCount: 63,
    projectCardsTotalCount: 50,
    cardsInCompleteColumnTotalCount: 37,
    projectCardsInCompleteColumnTotalCount: 35,
  },
];

data.map(
  (val) => (val.timestamp = new Date(val.timestamp).toISOString().slice(0, 10))
);
export default ({}) => {
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
