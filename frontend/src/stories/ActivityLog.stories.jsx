import React from "react";

import ActivityLog from "../components/regions/ActivityLog/Presentation";
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

const orderedDates = [
  "Sunday 21/03/2021",
  "Thursday 11/03/2021",
  "Monday 08/03/2021",
  "Wednesday 03/03/2021",
  "Tuesday 02/03/2021",
  "Monday 01/03/2021",
];

const activity = [
  {
    actorUser: 352,
    effectedUser: 802,
    eventColor: "#8e24aa",
    eventName: "Pull request review",
    eventType: 2,
    id: 116283,
    timestamp: "2022-09-02T13:46:16.295020Z",
    object1ContentTypeName: "git_real | pull request review",
    object1Id: 53534,
    object2ContentTypeName: "git_real | repository",
    object2Id: 7250,
  },
  {
    actorUser: 132,
    effectedUser: 896,
    eventColor: "#e53935",
    eventName: "Recruit project review",
    eventType: 1,
    id: 116282,
    timestamp: "2022-09-05T10:46:16.221191Z",
    object1ContentTypeName: "curriculum_tracking | recruit project review",
    object1Id: 45489,
    object2ContentTypeName: "curriculum_tracking | recruit project",
    object2Id: 15112,
  },
  {
    actorUser: 132,
    effectedUser: 1023,
    eventColor: "#e53935",
    eventType: 1,
    id: 116281,
    timestamp: "2022-09-01T13:18:03.743668Z",
    eventName: "Recruit project review",
    object1ContentTypeName: "curriculum_tracking | recruit project review",
    object1Id: 45488,
    object2ContentTypeName: "curriculum_tracking | recruit project",
    object2Id: 17024,
  },
];
export default {
  title: "Tilde/ActivityLog",
  component: ActivityLog,
};

const Template = (args) => <ActivityLog {...args} />;

export const Primary = Template.bind({});
Primary.args = {
  eventList: activity,
  orderedDates,
  eventTypesWithIds,
};
