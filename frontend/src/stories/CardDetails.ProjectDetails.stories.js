import React from "react";

import ProjectDetails from "../components/regions/CardDetails/ProjectDetails";
import reviewObject from "./fixtures/review.json";
import projectObject from "./fixtures/project.json";

export default {
  title: "Tilde/CardDetails/ProjectDetails",
  component: ProjectDetails,
  argTypes: {},
};

const Template = (args) => <ProjectDetails {...args} />;
export const Primary = Template.bind({});
Primary.args = {
  project: projectObject,
  reviews: [reviewObject],
  reviewIds: [1],
};
