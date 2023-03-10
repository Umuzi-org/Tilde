import React from "react";
import { ComponentStory, ComponentMeta } from "@storybook/react";

import Page from "./LoggedInPage";
import { Container } from "@mantine/core";

// More on default export: https://storybook.js.org/docs/react/writing-stories/introduction#default-export
export default {
  //   title: "components/LoggedInPage.tsx",
  component: Page,
  // More on argTypes: https://storybook.js.org/docs/react/api/argtypes
  argTypes: {},
} as ComponentMeta<typeof Page>;

// More on component templates: https://storybook.js.org/docs/react/writing-stories/introduction#using-args
const Template: ComponentStory<typeof Page> = (args) => {
  return (
    <Page {...args}>
      <Container>Content goes here</Container>
    </Page>
  );
};

export const Default = Template.bind({});
