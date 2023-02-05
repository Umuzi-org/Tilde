import React from "react";
import OutstandingReviewsUnconnected from "./index.jsx";
import { Provider } from "react-redux";
import { store } from "../../../redux/store";
import { outstandingCompetenceReviews } from "./storyData";

export default {
  title: "Tilde/regions/OutstandingReviewsModal",
  component: OutstandingReviewsUnconnected,
};

const Template = (args) => (
  <Provider store={store}>
    <OutstandingReviewsUnconnected {...args} />
  </Provider>
);

export const Full = Template.bind({});
Full.args = { outstandingCompetenceReviews, forceUser: 2 };
