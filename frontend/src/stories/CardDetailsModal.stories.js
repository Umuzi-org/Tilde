import React from "react";

import CardDetailsModal from "../components/regions/CardDetailsModal/Presentation";
import reviewObject from "./fixtures/review.json";
import repoProjectCard from "./fixtures/repoProjectCard.json";
import authUser from "./fixtures/authUser.json";

export default {
  title: "Tilde/CardDetailsModal/CardDetailsModal",
  component: CardDetailsModal,
  argTypes: {
    //   backgroundColor: { control: 'color' },
  },
};

const Template = (args) => <CardDetailsModal {...args} />;

export const Primary = Template.bind({});
Primary.args = {
  cardId: 1,
  card: repoProjectCard,
  authUser: authUser,
  reviews: [reviewObject],
  reviewIds: [1],
};
