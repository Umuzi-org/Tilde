import React from "react";
import { Paper, Grid } from "@material-ui/core";
import {
  BarChart,
  Bar,
  // Cell,
  // XAxis,
  // YAxis,
  // CartesianGrid,
  // Tooltip,
  // Legend,
  // ResponsiveContainer,
} from "recharts";
import { makeStyles } from "@material-ui/core/styles";
import {
  CARD_MOVED_TO_COMPLETE,
  CARD_MOVED_TO_REVIEW_FEEDBACK,
  CARD_REVIEW_REQUEST_CANCELLED,
  CARD_REVIEW_REQUESTED,
  CARD_STARTED,
  COMPETENCE_REVIEW_DONE,
  PR_REVIEWED,
} from "../../constants";
import { eventTypeColors } from "../../colors";
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
  {
    id: "date=2020-04-28&limit=20&offset=0&event_type__name=COMPETENCE_REVIEW_DONE&actor_user=2360",
    date: "2020-04-30",
    total: 3,
  },
];
const useStyles = makeStyles((theme) => ({
  paper: {
    // color: theme.palette.text.secondary,
  },
  containerStyles: {
    height: 20,
    width: "100%",
    backgroundColor: "#e0e0de",
    borderRadius: 50,
    margin: 50,
  },

  fillerStyles: {
    height: "100%",
    // width: `${completed}%`,
    // backgroundColor: `${bgcolor}`,
    borderRadius: "inherit",
    textAlign: "right",
  },

  labelStyles: {
    padding: 5,
    color: "white",
    fontWeight: "bold",
  },
}));
const result = getActivityLogCountsByDayForSingleUser({
  activityLogDayCounts,
  userId: 236,
  eventTypes: [
    ACTIVITY_LOG_EVENT_TYPE_COMPETENCE_REVIEW_DONE,
    ACTIVITY_LOG_EVENT_TYPE_PR_REVIEWED,
  ],
});

function Activity(props) {
  const classes = useStyles();
  const { bgColor, completed } = props; // fix names

  return (
    <div className={classes.containerStyles}>
      <div
        className={classes.fillerStyles}
        backgroundColor={bgColor}
        width={completed}
      >
        <span className={classes.labelStyles}>{completed}</span>
      </div>
    </div>
  );
}

console.log("hello", result);

export default ({ args }) => {
  const classes = useStyles();
  const testData = [
    { bgcolor: "#6a1b9a", completed: 60 },
    { bgcolor: "#00695c", completed: 30 },
    { bgcolor: "#ef6c00", completed: 53 },
  ];
  return (
    <div>
      {/* <BarChart width={150} height={40} data={result}>
        <Bar dataKey="COMPETENCE_REVIEW_DONE" fill="#8884d8" />
      </BarChart> */}
      <div className="App">
        {testData.map((item, idx) => (
          <Activity
            key={idx}
            bgcolor={item.bgcolor}
            completed={item.completed}
          />
        ))}
      </div>
      {/* <div>
        <Paper className={classes.paper}>log here</Paper>
        <Paper className={classes.paper}>log here</Paper>
        <Paper className={classes.paper}>log here</Paper>
        <Paper className={classes.paper}>log here</Paper>
        <Paper className={classes.paper}>log here</Paper>
        <Paper className={classes.paper}>log here</Paper>
      </div> */}
    </div>
  );
};

// const realData = [
//   {
//     id: 42,
//     event_type: 5,
//     actor_user: 18,
//     effected_user: 18,
//     object_1_content_type_name: "curriculum_tracking | recruit project",
//     object_1_id: 1,
//     object_2_content_type_name: null,
//     object_2_id: null,
//   },
//   {
//     id: 41,
//     event_type: 4,
//     actor_user: 18,
//     effected_user: 18,
//     object_1_content_type_name: "curriculum_tracking | recruit project review",
//     object_1_id: 14,
//     object_2_content_type_name: "curriculum_tracking | recruit project",
//     object_2_id: 1,
//   },
// ];
