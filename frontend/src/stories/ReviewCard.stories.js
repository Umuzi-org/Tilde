import React from "react";

import ReviewCard from "../components/widgets/ReviewCard";
import verboseReview from "./fixtures/verboseReview.json";

export default {
  title: "Tilde/ReviewCard",
  component: ReviewCard,
  // argTypes: {
  //   backgroundColor: { control: 'color' },
  // },
};

const Template = (args) => <ReviewCard {...args} />;

const review = {
  ...verboseReview,
  timestamp: new Date(verboseReview.timestamp),
};

export const Primary = Template.bind({});
Primary.args = {
  review,
};
