import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Paper from "@material-ui/core/Paper";
import Grid from "@material-ui/core/Grid";

import { eventTypeColors } from "../../../colors";

const useStyles = makeStyles((theme) => ({
  containerStyles: {
    width: "50%",
    margin: 10,
    border: "1px black solid",
  },

  fillerStyles: {
    height: "100%",
    textAlign: "right",
    // width: "10%",
    display: "flex",
    flexDirection: "row",
  },
  labelStyles: {
    // height: "100%",
    width: 20,
    color: "black",
    // fontWeight: 900,
  },
  content: {
    // height: "100%",
    // padding: 10,
    width: "90%",
  },
}));

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
    eventType: 2,
    actorUser: 352,
    effectedUser: 802,
    object1ContentTypeName: "git_real | pull request review",
    object1Id: 53534,
    object2ContentTypeName: "git_real | repository",
    object2Id: 7250,
  },
  {
    id: 116282,
    eventType: 1,
    actorUser: 132,
    effectedUser: 896,
    object1ContentTypeName: "curriculum_tracking | recruit project review",
    object1Id: 45489,
    object2ContentTypeName: "curriculum_tracking | recruit project",
    object2Id: 15112,
  },
  {
    id: 116281,
    eventType: 1,
    actorUser: 132,
    effectedUser: 1023,
    object1ContentTypeName: "curriculum_tracking | recruit project review",
    object1Id: 45488,
    object2ContentTypeName: "curriculum_tracking | recruit project",
    object2Id: 17024,
  },
];

const two = activity.map((item, index) => {
  let matchingIds = eventTypesWithIds.find(
    (elem) => elem.id === item.eventType
  );
  const result = {
    ...item,
    eventName: matchingIds ? matchingIds.name : "",
  };
  return result;
});

const v = () => {
  const arr = [];
  for (const color in eventTypeColors) {
    arr.push({ event: color, color: eventTypeColors[color] });
  }
  return arr;
};
const eventTypesWithColors = v();

const three = two.map((item, index) => {
  let matchingIds = eventTypesWithColors.find(
    (elem) => elem.event === item.eventName
  );
  const result = {
    ...item,
    eventColor: matchingIds ? matchingIds.color : "",
  };
  return result;
});

function LogBar({ color, event, object1ContentTypeName }) {
  const classes = useStyles();
  const adjustStyle = {
    backgroundColor: color,
  };
  return (
    <Grid className={classes.containerStyles}>
      <Grid className={classes.fillerStyles}>
        <span className={classes.labelStyles} style={adjustStyle} />
        <div className={classes.content}>
          <div>{event}</div>
          <div>{object1ContentTypeName}</div>
        </div>
      </Grid>
    </Grid>
  );
}
export default function Presentation() {
  return (
    <div>
      {three.map((item) => (
        <LogBar
          color={item.eventColor}
          event={item.eventName}
          object1ContentTypeName={item.object1ContentTypeName}
        />
      ))}
    </div>
  );
}
