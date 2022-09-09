import React from "react";
import Presentation from "./Presentation";

const eventTypeColors = {
  CARD_MOVED_TO_COMPLETE: "colors.yellow600",
  CARD_MOVED_TO_REVIEW_FEEDBACK: "colors.red600",
  CARD_REVIEW_REQUESTED: "colors.orange600",
  CARD_REVIEW_REQUEST_CANCELLED: "colors.grey600",
  CARD_STARTED: "colors.green600",
  PR_REVIEWED: "colors.purple600",
  COMPETENCE_REVIEW_DONE: "colors.blue600",
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
    event_type: 1,
    actorUser: 132,
    effectedUser: 896,
    object1ContentTypeName: "curriculum_tracking | recruit project review",
    object1Id: 45489,
    object2ContentTypeName: "curriculum_tracking | recruit project",
    object2Id: 15112,
  },
  {
    id: 116281,
    event_type: 1,
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
    (elem) => elem.id === item.event_type
  );
  const result = {
    ...item,
    eventName: matchingIds ? matchingIds.name : "",
  };
  return result;
});

// console.log(two);

const v = () => {
  const arr = [];
  for (const color in eventTypeColors) {
    arr.push({ event: color, color: eventTypeColors[color] });
  }
  return arr;
};
const eventTypesWithColors = v();
console.log(eventTypesWithColors);
console.log(two);
const three = activity.map((item, index) => {
  let matchingIds = eventTypesWithColors.find(
    (elem) => elem.eventName === item.event
  );
  const result = {
    ...item,
    eventColor: matchingIds ? matchingIds.color : "",
  };
  return result;
});

console.log(three);

export default () => {
  const props = {
    two,
    three,
  };
  return <Presentation {...props} />;
};
