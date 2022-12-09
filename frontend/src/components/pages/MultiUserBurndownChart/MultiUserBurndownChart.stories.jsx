import React from "react";

import multiUserBurndownData from "./storyData/multiUserBurnDownData.json";
import { MultiUserBurndownChartUnconnected } from ".";

export default {
  title: "Tilde/pages/MultiUserBurndownChart",
  component: MultiUserBurndownChartUnconnected,
};

const Template = (args) => (
  <MultiUserBurndownChartUnconnected {...args} />
);

export const Primary = Template.bind({});

Primary.args = {
  team: multiUserBurndownData.team,
  // mapStateToProps
  currentTeamBurndownStats: multiUserBurndownData.teamBurnDownStats,

  // mapDispatchToProps

  // storybook
};
