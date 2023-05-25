import React from "react";

import { ActionReviewedCard } from "../components/widgets/ActionLogCards";
import verboseReview from "./fixtures/verboseReview.json";

export default {
  title: "Tilde/ActionReviewedCard",
  component: ActionReviewedCard,
  // argTypes: {
  //   backgroundColor: { control: 'color' },
  // },
};

const Template = (args) => <ActionReviewedCard {...args} />;

const review = {
  ...verboseReview,
  timestamp: new Date(verboseReview.timestamp),
};

export const Primary = Template.bind({});
Primary.args = {
  review,
};
