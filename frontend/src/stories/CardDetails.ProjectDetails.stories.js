import React from "react";

import ProjectDetails from "../components/pages/CardDetails/ProjectDetails";
import reviewObject from "./fixtures/review.json";
import projectObject from "./fixtures/project.json";
import { Provider } from "react-redux";
import { store } from "../redux/store";

export default {
  title: "Tilde/pages/CardDetails/ProjectDetails",
  component: ProjectDetails,
  argTypes: {},
};

const Template = (args) => (
  <Provider store={store}>
    <ProjectDetails {...args} />
  </Provider>
);
export const Primary = Template.bind({});
Primary.args = {
  project: projectObject,
  reviews: [reviewObject],
};
