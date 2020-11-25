import React from 'react';

import ProjectDetails from "../components/regions/CardDetailsModal/ProjectDetails"
import reviewObject from "./assets/review.json"
import projectObject from "./assets/project.json"

export default {
    title: 'Tilde/CardDetailsModal/ProjectDetails',
    component: ProjectDetails,
    argTypes: {
    },
  };


  const Template = (args) => <ProjectDetails {...args} />;
  export const Primary = Template.bind({});
  Primary.args = {
    project: projectObject,
    reviews: [reviewObject],
    reviewIds: [1]
  };
  
