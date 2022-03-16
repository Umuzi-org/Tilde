import React from "react";

import CardDetails from "../components/pages/CardDetails/Presentation";
import reviewObject from "./fixtures/review.json";
import repoProjectCard from "./fixtures/repoProjectCard.json";

export default {
  title: "Tilde/pages/CardDetails/CardDetails",
  component: CardDetails,
  argTypes: {
    //   backgroundColor: { control: 'color' },
  },
};

const Template = (args) => <CardDetails {...args} />;

export const Primary = Template.bind({});
Primary.args = {
  cardId: 1,
  card: repoProjectCard,
  reviews: [reviewObject],
  reviewIds: [1],
};
