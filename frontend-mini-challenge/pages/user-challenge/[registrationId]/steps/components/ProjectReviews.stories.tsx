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

const errorComments = `Something went wrong blah blah blah etc

Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
`;

export const NoReviews = Template.bind({});
NoReviews.args = {
  reviews: [],
};

export const Positive = Template.bind({});
Positive.args = {
  reviews: [
    {
      timestamp: "2023-03-02T15:27:37Z",
      status: COMPETENT,
      comments: "Looks good",
    },
    {
      timestamp: "2023-03-01T15:27:37Z",
      status: NOT_YET_COMPETENT,
      comments: errorComments,
    },
  ],
};

export const Negative = Template.bind({});
Negative.args = {
  reviews: [
    {
      timestamp: "2023-03-02T15:27:37Z",
      status: NOT_YET_COMPETENT,
      comments: errorComments,
    },
  ],
};

export const Reviewing = Template.bind({});
Reviewing.args = {
  status: STATUS_UNDER_REVIEW,
  reviews: [
    {
      timestamp: "2023-03-02T15:27:37Z",
      status: NOT_YET_COMPETENT,
      comments: errorComments,
    },
  ],
};
