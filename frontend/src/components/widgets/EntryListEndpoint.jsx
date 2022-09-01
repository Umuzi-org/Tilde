import React from "react";
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
import { apiReduxWatchers } from "../../apiAccess/apiApps";

const useStyles = makeStyles((theme) => ({
  containerStyles: {
    height: "100%",
    width: "50%",
    backgroundColor: "#D3D3D3",
    borderRadius: 40,
    margin: 50,
  },

  fillerStyles: {
    height: "100%",
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
    <div className={classes.containerStyles}>
      <div className={classes.fillerStyles} style={adjustStyle}>
        <span className={classes.labelStyles} />
      </div>
    </div>
  );
};

const events = {
  CARD_MOVED_TO_COMPLETE,
  CARD_MOVED_TO_REVIEW_FEEDBACK,
  CARD_REVIEW_REQUEST_CANCELLED,
  CARD_REVIEW_REQUESTED,
  CARD_STARTED,
  COMPETENCE_REVIEW_DONE,
  PR_REVIEWED,
};
// console.log(eventTypeColors);

const sortData = ({ eventTypes, eventTypeColors }) => {
  const arr = [];
  for (const type in eventTypes) {
    arr.push({
      event: type,
      eventColor: eventTypeColors[type],
      total: 10,
    });
  }
  return arr;
};

const one = [
  {
    id: "date=2022-09-01&event_type=2&filter_by_actor_user=None&filter_by_effected_user=None",
    date: "2022-09-01",
    total: 3,
    filter_by_actor_user: null,
    filter_by_effected_user: null,
    event_type: 2,
    color: "red",
  },
  {
    id: "date=2022-09-01&event_type=4&filter_by_actor_user=None&filter_by_effected_user=None",
    date: "2022-09-01",
    total: 5,
    filter_by_actor_user: null,
    filter_by_effected_user: null,
    event_type: 4,
    color: "blue",
  },
  {
    id: "date=2022-09-01&event_type=6&filter_by_actor_user=None&filter_by_effected_user=None",
    date: "2022-09-01",
    total: 4,
    filter_by_actor_user: null,
    filter_by_effected_user: null,
    event_type: 6,
    color: "pink",
  },
];

console.log("hello", sortData({ eventTypes: events, eventTypeColors }));
const test = sortData({ eventTypes: events, eventTypeColors });
// console.log("hello", eventTypeColors);
export default ({ args }) => {
  return (
    <div>
      <div>
        {one.map((item, idx) => (
          <ProgressBar key={idx} progress={item.total} bgColor={item.color} />
        ))}
      </div>
    </div>
  );
};
