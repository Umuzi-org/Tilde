import React from "react";
import AgileCard from "../components/regions/AgileBoard/AgileCard/Presentation"; 

import assigneeCard from "./fixtures/AgileCards/assigneeCard.json";
import reviewerCard from "./fixtures/AgileCards/reviewerCard.json";
import openPrCard from "./fixtures/AgileCards/openPrCard.json";
import reviewEmojiesCard from "./fixtures/AgileCards/reviewEmojisCard.json";
import topicCard from "./fixtures/AgileCards/topicCard.json";
import blockedCard from "./fixtures/AgileCards/blockedCard.json"

import user from "./fixtures/user.json";
import authUser from "./fixtures/authUser.json";

export default {
    title: "Tilde/AgileCard",
    component: AgileCard
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

export const TopicCard = Template.bind({});
TopicCard.args = {
  ...Assignee.args,
  card: topicCard,
}

export const BlockedCard = Template.bind({});
BlockedCard.args = {
  ...Assignee.args,
  card: blockedCard,
}