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
export default {
  title: "Tilde/ActivityLog",
  component: ActivityLog,
};

const Template = (args) => <ActivityLog {...args} />;

export const Primary = Template.bind({});
Primary.args = {};
