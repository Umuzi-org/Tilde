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
console.log("hello", result[0].COMPETENCE_REVIEW_DONE);

export default ({ args }) => {
  const classes = useStyles();
  // console.log("hello", UserActions({ args }));
  // return <Grid>hello</Grid>;
  return (
    <div className={classes.column}>
      <ResponsiveContainer>
        <BarChart width={150} height={40} data={result}>
          dl
          {/* <Bar dataKey="uv" fill="#8884d8" /> fkj */}
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};
