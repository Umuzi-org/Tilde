import React from "react";
import { BrowserRouter as Router } from "react-router-dom";

import multiUserBurndownData from "./storyData/multiUserBurnDownData.json";
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
  currentTeamBurndownStats: multiUserBurndownData.teamBurnDownStats,
  team: multiUserBurndownData.team,
  metrics: multiUserBurndownData.metrics,

  // mapDispatchToProps

  // storybook
};
