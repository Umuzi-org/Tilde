import React from "react";

import CardDetails from "../components/regions/CardDetails/Presentation";
import reviewObject from "./fixtures/review.json";
import repoProjectCard from "./fixtures/repoProjectCard.json";

export default {
  title: "Tilde/CardDetails/CardDetails",
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
