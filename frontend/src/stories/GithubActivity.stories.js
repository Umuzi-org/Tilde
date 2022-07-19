import React from "react";

import GithubActivity from "../components/pages/UserActions/GithubActivity";

const dates = [
  "Mon 1 ",
  "Tues 1",
  "Wed 1",
  "Thurs 1",
  "Fri 1",
  "Sat 1",
  "Sun 1",
  "Mon 2",
  "Tues 2",
  "Wed 2",
  "Thurs 2",
  "Fri 2",
  "Sat 2",
  "Sun 2",
];

const eventTypes = [
  "Push",
  "PullRequestReview",
  "TildeCardReview",
  "TildeCardComplete",
];

const activityLog = eventTypes.map((eventType) => {
  return {
    x: [...dates],
    y: dates.map(() => Math.floor(Math.random() * 20)),
    name: eventType,
    meta: dates.map(() => (
      <ul>
        <li>Metadata blah blah</li>
        <li>Metadata blah blah</li>
        <li>Metadata blah blah</li>
      </ul>
    )),
  };
});

export default {
  title: "Tilde/pages/GithubActivity",
  component: GithubActivity,
};

const Template = (args) => <GithubActivity {...args} />;

export const Primary = Template.bind({});
Primary.args = {
  activityLog,
};
