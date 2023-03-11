import { ComponentStory, ComponentMeta } from "@storybook/react";

import ProjectReviews from "./ProjectReviews";
import {
  COMPETENT,
  NOT_YET_COMPETENT,
  STATUS_UNDER_REVIEW,
} from "../../../../../constants";

export default {
  component: ProjectReviews,
  argTypes: {},
} as ComponentMeta<typeof ProjectReviews>;

const Template: ComponentStory<typeof ProjectReviews> = (args) => {
  return <ProjectReviews {...args} />;
};

export const NoReviews = Template.bind({});
NoReviews.args = {};

export const Positive = Template.bind({});
Positive.args = {
  review: {
    timestamp: "2023-03-02T15:27:37Z",
    status: COMPETENT,
    comments: "Looks good",
  },
};

export const Negative = Template.bind({});
Positive.args = {
  review: {
    timestamp: "2023-03-02T15:27:37Z",
    status: NOT_YET_COMPETENT,
    comments: "Something went wrong blah blah blah etc",
  },
};

export const Reviewing = Template.bind({});
Reviewing.args = {
  status: STATUS_UNDER_REVIEW,
  review: {
    timestamp: "2023-03-02T15:27:37Z",
    status: NOT_YET_COMPETENT,
    comments: "Something went wrong blah blah blah etc",
  },
};
