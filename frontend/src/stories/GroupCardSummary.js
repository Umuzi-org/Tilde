import React from "react";

import { GroupCardSummary } from "../components/regions/GroupCardSummary/Presentation";

export default {
  title: "Tilde/GroupCardSummary",
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
};
