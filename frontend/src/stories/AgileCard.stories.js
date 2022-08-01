import React from "react";
import AgileCard from "../components/pages/AgileBoard/AgileCard/Presentation"; 

import agileCard from "./fixtures/agileCard.json";
import assigneeCard from "./fixtures/AgileCards/assigneeCard.json";
import reviewerCard from "./fixtures/AgileCards/reviewerCard.json";
import openPrCard from "./fixtures/AgileCards/openPrCard.json";
import reviewEmojiesCard from "./fixtures/AgileCards/reviewEmojisCard.json";
import topicCard from "./fixtures/AgileCards/topicCard.json";
import inReviewCard from "./fixtures/AgileCards/inReviewCard.json";
import blockedCard from "./fixtures/AgileCards/blockedCard.json";
import dueTimeCard from "./fixtures/AgileCards/dueTimeCard.json"

import user from "./fixtures/user.json";
import authUser from "./fixtures/authUser.json";

export default {
    title: "Tilde/pages/AgileCard",
    component: AgileCard,
}

const Template = args => <AgileCard {...args} />

export const Primary = Template.bind({});
Primary.args = {
  card: agileCard,
  authUser: authUser,
  viewedUser: user,
  filterUserId: user.id,

  handleClickAddReview: () => {},
  handleClickOpenCardDetails: () => {},
  handleRequestReview: () => {},
  handleStartProject: () => {},
  handleCancelReviewRequest: () => {},
  handleClickOpenWorkshopAttendanceForm: () => {},
  handleStartTopic: () => {},
  handleStopTopic: () => {},
  handleFinishTopic: () => {},
  handleRemoveWorkshopAttendance: () => {},

  loadingStartProject: false,
  loadingStartTopic: false,
  loadingClickOpenWorkshopAttendanceForm: false,
  loadingRequestReview: false,
  loadingCancelReviewRequest: false,
  loadingStopTopic: false,
  loadingFinishTopic: false,
  loadingRemoveWorkshopAttendance: false,
}

export const AssigneeBlue = Template.bind({});
AssigneeBlue.args = {
  ...Primary.args,
  card: assigneeCard,
}

export const ReviewerOrange = Template.bind({});
ReviewerOrange.args = {
  ...Primary.args,
  card: reviewerCard,
}

export const OpenPullRequest = Template.bind({});
OpenPullRequest.args = {
  ...Primary.args,
  card: openPrCard,
}

export const ReviewEmojies = Template.bind({});
ReviewEmojies.args = {
  ...Primary.args,
  card: reviewEmojiesCard,
}

export const StatusBlocked = Template.bind({});
StatusBlocked.args = {
  ...Primary.args,
  card: blockedCard,
}

export const StatusReady = Template.bind({});
StatusReady.args = {
  ...Primary.args,
  card: topicCard,
}

export const StatusInProgress = Template.bind({});
StatusInProgress.args = {
  ...Primary.args,
  card: openPrCard,
}

export const StatusInReview = Template.bind({});
StatusInReview.args = {
  ...Primary.args,
  card: inReviewCard,
}

export const StatusFeedback = Template.bind({});
StatusFeedback.args = {
  ...Primary.args,
  card: reviewEmojiesCard,
}

export const DueTime = Template.bind({});
DueTime.args = {
  ...Primary.args,
  card: dueTimeCard,
}
