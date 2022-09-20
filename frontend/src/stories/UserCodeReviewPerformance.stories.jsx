import React from "react";
import UserCodeReviewPerformance from "../components/pages/UserCodeReviewPerformance/Presentation";
import competenceReviews from "./fixtures/codeReviewQualityList.json";
import { BrowserRouter as Router } from "react-router-dom";

export default {
  title: "Tilde/pages/UserCodeReviewPerformance",
  component: UserCodeReviewPerformance,
};

const Template = (args) => (
  <Router>
    <UserCodeReviewPerformance {...args} />{" "}
  </Router>
);

export const Primary = Template.bind({});

Primary.args = {
  competenceReviews,
};
