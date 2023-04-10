import React from "react";
import { ComponentStory, ComponentMeta } from "@storybook/react";
import {
  STATUS_READY,
  STATUS_BLOCKED,
  STATUS_DONE,
  STATUS_UNDER_REVIEW,
  STATUS_ERROR,
} from "../../../../constants";

import Step from "./Step";
import { Stack } from "@mantine/core";

// More on default export: https://storybook.js.org/docs/react/writing-stories/introduction#default-export
export default {
  component: Step,
  // More on argTypes: https://storybook.js.org/docs/react/api/argtypes
  argTypes: {},
} as ComponentMeta<typeof Step>;

// More on component templates: https://storybook.js.org/docs/react/writing-stories/introduction#using-args
const Template: ComponentStory<typeof Step> = (args) => {
  return <Step {...args} />;
};

const title = "Eat that frog!";
const blurb =
  "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. ";
const index = 2;

// More on args: https://storybook.js.org/docs/react/writing-stories/args
export const Ready = Template.bind({});
Ready.args = {
  index,
  title,
  blurb,
  status: STATUS_READY,
};

export const Blocked = Template.bind({});
Blocked.args = {
  index,
  title,
  blurb,
  status: STATUS_BLOCKED,
};

export const Done = Template.bind({});
Done.args = {
  index,
  title,
  blurb,
  status: STATUS_DONE,
};

export const Review = Template.bind({});
Review.args = {
  index,
  title,
  blurb,
  status: STATUS_UNDER_REVIEW,
};

export const Error = Template.bind({});
Error.args = {
  index,
  title,
  blurb,
  status: STATUS_ERROR,
};

// export function AllSteps() {
//   return (
//     <Stack>
//       <Template {...Done.args} />
//       <Template {...Error.args} />
//       <Template {...Ready.args} />
//       <Template {...Blocked.args} />
//       <Template {...Review.args} />
//     </Stack>
//   );
// }
