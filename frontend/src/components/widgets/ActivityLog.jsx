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

const useStyles = makeStyles((theme) => ({
  containerStyles: {
    width: "50%",
    backgroundColor: "#D3D3D3",
    margin: 50,
  },

  fillerStyles: {
    height: "100%",
    textAlign: "right",
    width: "10%",
  },

  labelStyles: {
    height: "100%",
    padding: 10,
    color: "black",
    fontWeight: 900,
  },
}));

const ActionList = ({ bgColor, totalNumberOfActions }) => {
  const classes = useStyles();
  const specificColor = { backgroundColor: bgColor };

  return (
    <div className={classes.containerStyles}>
      <div className={classes.fillerStyles} style={specificColor}>
        <div className={classes.labelStyles} />
        <div>{totalNumberOfActions}</div>
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
const eventTypesWithIds = [
  {
    id: 5,
    name: "CARD_MOVED_TO_COMPLETE",
  },
  {
    id: 6,
    name: "CARD_MOVED_TO_REVIEW_FEEDBACK",
  },
  {
    id: 3,
    name: "CARD_REVIEW_REQUEST_CANCELLED",
  },
  {
    id: 2,
    name: "CARD_REVIEW_REQUESTED",
  },
  {
    id: 1,
    name: "CARD_STARTED",
  },
  {
    id: 4,
    name: "COMPETENCE_REVIEW_DONE",
  },
];
const activity = [
  {
    id: "date=2022-09-01&event_type=2&filter_by_actor_user=None&filter_by_effected_user=None",
    date: "2022-09-01",
    total: 3,
    filter_by_actor_user: null,
    filter_by_effected_user: null,
    event_type: 2,
  },
  {
    id: "date=2022-09-01&event_type=4&filter_by_actor_user=None&filter_by_effected_user=None",
    date: "2022-09-01",
    total: 5,
    filter_by_actor_user: null,
    filter_by_effected_user: null,
    event_type: 4,
  },
  {
    id: "date=2022-09-01&event_type=6&filter_by_actor_user=None&filter_by_effected_user=None",
    date: "2022-09-01",
    total: 4,
    filter_by_actor_user: null,
    filter_by_effected_user: null,
    event_type: 6,
  },
];

const newData = eventTypesWithIds.map((item, index) => {
  return {
    ...item,
    name: activity.find((elem) => elem.event_type === item.id) ? item.name : "",
  };
});

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
const test = sortData({ eventTypes: events, eventTypeColors });

const two = test.map((item, index) => {
  const result = {
    ...item,
    color: newData.find((elem) => elem.eventTypes === item.eventTypes)
      ? item.eventColor
      : "",
  };
  return result;
});
console.log("hello", two);

export default ({ args }) => {
  return (
    <div>
      <div>
        {two.map((item, idx) => (
          <ActionList
            key={idx}
            // totalNumberOfActions={item.total}
            bgColor={item.color}
          />
        ))}
      </div>
    </div>
  );
};
