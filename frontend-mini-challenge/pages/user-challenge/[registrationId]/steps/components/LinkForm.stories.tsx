import { ComponentStory, ComponentMeta } from "@storybook/react";

import LinkForm from "./LinkForm";

export default {
  component: LinkForm,
  // More on argTypes: https://storybook.js.org/docs/react/api/argtypes
  argTypes: {},
} as ComponentMeta<typeof LinkForm>;

const Template: ComponentStory<typeof LinkForm> = (args) => {
  return <LinkForm {...args} />;
};

export const Blank = Template.bind({});
Blank.args = {
  linkSubmission: "",
  linkExample: "https://your.link/whatevs",
  linkName: "Your submission link",
  //   status: 200,
  //   responseData: {},
};

export const Success = Template.bind({});
Success.args = {
  linkSubmission: "https://your.link/whatevs",
  linkExample: "https://your.link/whatevs",
  linkName: "Your submission link",
  status: 200,
  responseData: {},
};

export const Error = Template.bind({});
Error.args = {
  linkSubmission: "https://your.link/whatevs",
  linkExample: "https://your.link/whatevs",
  linkName: "Your submission link",
  status: 400,
  responseData: {
    linkSubmission: "This is an error from the server",
  },
};

export const Loading = Template.bind({});
Loading.args = {
  linkSubmission: "",
  linkExample: "https://your.link/whatevs",
  linkName: "Your submission link",
  isLoading: true,
};
