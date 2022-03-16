import React from "react";
import Review from "../components/pages/CardDetails/Review";
import review from "./fixtures/review.json";

export default {
  title: "Tilde/pages/CardDetails/Review",
  component: Review,
};

const Template = (args) => <Review {...args} />;
export const Primary = Template.bind({});
Primary.args = {
  review,
};
