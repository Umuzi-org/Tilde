import React from "react";
import { BrowserRouter as Router } from "react-router-dom";

import allReviews from "./storyData/allReviews.json";
import { UserCodeReviewPerformanceUnconnected } from ".";

export default {
  title: "Tilde/pages/UserCodeReviewPerformance",
  component: UserCodeReviewPerformanceUnconnected,
};

const Template = (args) => (
  <Router>
    <UserCodeReviewPerformanceUnconnected {...args} />{" "}
  </Router>
);

export const Primary = Template.bind({});

Primary.args = {
  // mapStateToProps

  competenceReviewsObject: allReviews.competenceReviewsObject,
  pullRequestReviewsObject: allReviews.pullRequestReviewsObject,

  // mapDispatchToProps
  fetchCompetenceReviewQualityPage: () => {},
  fetchPullRequestQualitiesPage: () => {},

  // storybook
  forceUser: 219,
  forceToday: "2022-09-23T07:51:27Z",
};
