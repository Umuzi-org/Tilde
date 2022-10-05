import React from "react";
import { BrowserRouter as Router } from "react-router-dom";

import userBurndownStats from "./storyData/burnDownData.json";
import { MultiUserBurndownChartUnconnected } from ".";

export default {
  title: "Tilde/pages/MultiUserBurndownChart",
  component: MultiUserBurndownChartUnconnected,
};

const Template = (args) => (
  <Router>
    <MultiUserBurndownChartUnconnected {...args} />{" "}
  </Router>
);

export const Primary = Template.bind({});

Primary.args = {
  // mapStateToProps
  currentUserBurndownStats: userBurndownStats,

  // mapDispatchToProps

  // storybook
  forceUser: 1,
};
