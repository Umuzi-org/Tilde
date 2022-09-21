import React from "react";
import GlobalCodeReviewDashboard from "../components/pages/GlobalCodeReviewDashboard/Presentation";

import codeReviewQueueProjects from "./fixtures/codeReviewQueueProjects.json";

export default {
  title: "Tilde/pages/GlobalCodeReviewDashboard",
  component: GlobalCodeReviewDashboard,
};

const Template = (args) => <GlobalCodeReviewDashboard {...args} />;

export const Primary = Template.bind({});

Primary.args = {
  competenceReviewQueueProjects: codeReviewQueueProjects,
  pullRequestReviewQueueProjects: codeReviewQueueProjects,
  // filterIncludeTags: ["clustering"],
  // filterExcludeTags: ["data structures"],

  // filterIncludeFlavours: ["python"],
  // filterExcludeFlavours: ["python"],

  handleChangeFlavourFilter: () => {},
  handleChangeTagFilter: () => {},
};
