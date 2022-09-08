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

const events = {
  CARD_MOVED_TO_COMPLETE,
  CARD_MOVED_TO_REVIEW_FEEDBACK,
  CARD_REVIEW_REQUEST_CANCELLED,
  CARD_REVIEW_REQUESTED,
  CARD_STARTED,
  COMPETENCE_REVIEW_DONE,
  PR_REVIEWED,
};

const useStyles = makeStyles((theme) => ({
  containerStyles: {
    width: "50%",
    margin: 10,
    border: "1px black solid",
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

const mapColorsWithEventTypes = test.map((item, index) => {
  const result = {
    ...item,
    color: newData.find((elem) => elem.eventTypes === item.eventTypes)
      ? item.eventColor
      : "",
  };
  return result;
});

export default ({ args }) => {
  return (
    <div>
      <div>
        {mapColorsWithEventTypes.map((item, idx) => (
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
