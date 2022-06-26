import React from "react";

import GroupCardSummary from "../components/pages/GroupCardSummary/Presentation";
import verboseReview from "./fixtures/verboseReview.json";
import users from "./fixtures/allUsers.json";
import teams from "./fixtures/allTeams.json";

export default {
  title: "Tilde/pages/GroupCardSummary",
  component: GroupCardSummary,
  // argTypes: {
  //   backgroundColor: { control: 'color' },
  // },
};

const Template = (args) => <GroupCardSummary {...args} />;

const review = {
  ...verboseReview,
  timestamp: new Date(verboseReview.timestamp),
};

export const Primary = Template.bind({});
Primary.args = {
  review,
  teams,
  users,
  userGroup: {},
  columns: [],
};
