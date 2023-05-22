import React from "react";
import { ComponentStory, ComponentMeta } from "@storybook/react";

import { Presentation } from "./LoggedInPage";
import { Text } from "@mantine/core";

// More on default export: https://storybook.js.org/docs/react/writing-stories/introduction#default-export
export default {
  component: Presentation,
  // More on argTypes: https://storybook.js.org/docs/react/api/argtypes
  argTypes: {},
} as ComponentMeta<typeof Presentation>;

// More on component templates: https://storybook.js.org/docs/react/writing-stories/introduction#using-args
const Template: ComponentStory<typeof Presentation> = (args) => {
  return (
    <Presentation {...args}>
      <Text>Content goes here</Text>
    </Presentation>
  );
};

export const Loaded = Template.bind({});
Loaded.args = {
  loggedInUserData: { firstName: "Applejuice", email: "email" },
  handleLogout: () => {},
};
