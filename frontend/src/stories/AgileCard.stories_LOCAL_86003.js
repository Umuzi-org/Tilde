import React from "react";
import AgileCard from "../components/regions/AgileBoard/AgileCard/Presentation"; 

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
    title: "Tilde/AgileCard",
    component: AgileCard,
}

const Template = args => <AgileCard {...args} />

export const Assignee = Template.bind({});
Assignee.args = {
  card: assigneeCard,
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

export const Reviewer = Template.bind({});
Reviewer.args = {
  ...Assignee.args,
  card: reviewerCard,
}

export const OpenPullRequest = Template.bind({});
OpenPullRequest.args = {
  ...Assignee.args,
  card: openPrCard,
}

export const ReviewEmojies = Template.bind({});
ReviewEmojies.args = {
  ...Assignee.args,
  card: reviewEmojiesCard,
}

export const StatusBlocked = Template.bind({});
StatusBlocked.args = {
  ...Assignee.args,
  card: blockedCard,
}

export const StatusReady = Template.bind({});
StatusReady.args = {
  ...Assignee.args,
  card: topicCard,
}

export const StatusInProgress = Template.bind({});
StatusInProgress.args = {
  ...Assignee.args,
  card: openPrCard,
}

export const StatusInReview = Template.bind({});
StatusInReview.args = {
  ...Assignee.args,
  card: inReviewCard,
}

export const StatusFeedback = Template.bind({});
StatusFeedback.args = {
  ...Assignee.args,
  card: reviewEmojiesCard,
}

export const DueTime = Template.bind({});
DueTime.args = {
  ...Assignee.args,
  card: dueTimeCard,
}