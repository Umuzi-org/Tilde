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

const useStyles = makeStyles((theme) => ({
  // paper: {
  //   // color: theme.palette.text.secondary,
  // },
  containerStyles: {
    height: "100%",
    width: "100%",
    backgroundColor: "whitesmoke",
    borderRadius: 40,
    margin: 50,
  },

  fillerStyles: {
    height: "100%",
    // width: `${progress}%`,
    // backgroundColor: bgColor,
    borderRadius: 40,
    textAlign: "right",
  },

  labelStyles: {
    padding: 10,
    color: "black",
    fontWeight: 900,
  },
}));

const ProgressBar = ({ bgColor, progress }) => {
  const classes = useStyles();

  const adjustStyle = {
    width: `${progress}%`,
    backgroundColor: bgColor,
  };

  return (
    <div className={classes.containerStyles} style={adjustStyle}>
      <div className={classes.fillerStyles}>
        <span className={classes.labelStyles} />
      </div>
    </div>
  );
};
const testData = [
  { bgColor: "#6a1b9a", completed: 60 },
  { bgColor: "#00695c", completed: 30 },
  { bgColor: "#ef6c00", completed: 53 },
  { bgColor: "#ef6c00", completed: 53 },
  { bgColor: "#ef6c00", completed: 53 },
];

const mockData = [
  {
    id: "date=2022-09-01&event_type=2&filter_by_actor_user=None&filter_by_effected_user=None",
    date: "2022-09-01",
    total: 3,
    filter_by_actor_user: null,
    filter_by_effected_user: null,
    event_type: 2,
    color: "#6a1b9a",
  },
  {
    id: "date=2022-09-01&event_type=4&filter_by_actor_user=None&filter_by_effected_user=None",
    date: "2022-09-01",
    total: 5,
    filter_by_actor_user: null,
    filter_by_effected_user: null,
    event_type: 4,
    color: "#6a1b9a",
  },
  {
    id: "date=2022-09-01&event_type=6&filter_by_actor_user=None&filter_by_effected_user=None",
    date: "2022-09-01",
    total: 4,
    filter_by_actor_user: null,
    filter_by_effected_user: null,
    event_type: 6,
    color: "#ef6c00",
  },
  {
    id: "date=2022-08-31&event_type=2&filter_by_actor_user=None&filter_by_effected_user=None",
    date: "2022-08-31",
    total: 5,
    filter_by_actor_user: null,
    filter_by_effected_user: null,
    event_type: 2,
    color: "#6a1b9a",
  },
];
export default ({ args }) => {
  const classes = useStyles();

  return (
    <div>
      <div>
        {mockData.map((item, idx) => (
          <ProgressBar
            key={idx}
            max="100"
            progress={item.total}
            height="100"
            bgColor={item.color}
          />
        ))}
      </div>
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
