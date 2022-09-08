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
    id: 116283,
    event_type: 2,
    actor_user: 352,
    effected_user: 802,
    object_1_content_type_name: "git_real | pull request review",
    object_1_id: 53534,
    object_2_content_type_name: "git_real | repository",
    object_2_id: 7250,
  },
  {
    id: 116282,
    event_type: 1,
    actor_user: 132,
    effected_user: 896,
    object_1_content_type_name: "curriculum_tracking | recruit project review",
    object_1_id: 45489,
    object_2_content_type_name: "curriculum_tracking | recruit project",
    object_2_id: 15112,
  },
  {
    id: 116281,
    event_type: 1,
    actor_user: 132,
    effected_user: 1023,
    object_1_content_type_name: "curriculum_tracking | recruit project review",
    object_1_id: 45488,
    object_2_content_type_name: "curriculum_tracking | recruit project",
    object_2_id: 17024,
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
