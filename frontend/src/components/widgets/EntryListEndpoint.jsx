import React from "react";
import { Typography, Paper, Grid } from "@material-ui/core";
import {
  BarChart,
  Bar,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

import { makeStyles } from "@material-ui/core/styles";

// import UserActions from "../regions/UserActions/Presentation";
// import apis from "../../apiAccess/apis";
import { getActivityLogCountsByDayForSingleUser } from "../../apiAccess/selectors/activityLogSelectors";
import {
  ACTIVITY_LOG_EVENT_TYPE_COMPETENCE_REVIEW_DONE,
  ACTIVITY_LOG_EVENT_TYPE_PR_REVIEWED,
} from "../../constants";
const activityLogDayCounts = [
  {
    id: "date=2020-04-28&limit=20&offset=0&event_type__name=COMPETENCE_REVIEW_DONE&actor_user=236",
    date: "2020-04-28",
    total: 1,
  },
  {
    id: "date=2020-04-28&limit=20&offset=0&event_type__name=COMPETENCE_REVIEW_DONE&actor_user=2360",
    date: "2020-04-29",
    total: 1,
  },
];
const result = getActivityLogCountsByDayForSingleUser({
  activityLogDayCounts,
  userId: 236,
  eventTypes: [
    ACTIVITY_LOG_EVENT_TYPE_COMPETENCE_REVIEW_DONE,
    ACTIVITY_LOG_EVENT_TYPE_PR_REVIEWED,
  ],
});
const useStyles = makeStyles((theme) => ({}));
const data = [
  {
    s: "Page A",
    uv: 4000,
    pv: 2400,
    amt: 2400,
  },
  {
    s: "Page B",
    uv: 3000,
    pv: 1398,
    amt: 2210,
  },
  {
    s: "Page C",
    uv: 2000,
    pv: 9800,
    amt: 2290,
  },
  {
    s: "Page D",
    uv: 2780,
    pv: 3908,
    amt: 2000,
  },
  {
    s: "Page E",
    uv: 1890,
    pv: 4800,
    amt: 2181,
  },
  {
    s: "Page F",
    uv: 2390,
    pv: 3800,
    amt: 2500,
  },
  {
    s: "Page G",
    uv: 3490,
    pv: 4300,
    amt: 2100,
  },
];

console.log("hello", data);

export default ({ args }) => {
  const classes = useStyles();
  // console.log("hello", UserActions({ args }));
  // return <Grid>hello</Grid>;
  return (
    <div>
      {/* <ResponsiveContainer> */}
      <BarChart width={150} height={40} data={data}>
        <Bar dataKey="uv" fill="#8884d8" />
      </BarChart>
      {/* </ResponsiveContainer> */}
    </div>
  );
};
