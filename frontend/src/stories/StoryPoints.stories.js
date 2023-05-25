import React from "react";

import StoryPoints from "../components/widgets/StoryPoints";

export default {
  title: "Tilde/StoryPoints",
  component: StoryPoints,
  // argTypes: {
  //   backgroundColor: { control: 'color' },
  // },
};

const Template = (args) => <StoryPoints {...args} />;

export const Primary = Template.bind({});
Primary.args = {
  storyPoints: 13,
};
