import React from "react";

import GithubAcivity from "../components/regions/UserActions/GithubAcivity";
// import activityLog from "./assets/githubUserActivity.json"

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
  // "Mon 3","Tues 3", "Wed 3","Thurs 3", "Fri 3", "Sat 3", "Sun 3"
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

// const activityLog = [

//     {
//         x: [...dates],
//         y: dates.map(()=>Math.random()),
//         meta: dates.map(()=>Math.random()),
//         name: 'PushEvent',

//       },

//       {
//         x: [...dates],
//         y: dates.map(()=>Math.random()),
//         meta: dates.map(()=>Math.random()),
//         name: 'CreateEvent',
//       },

//       {
//         x: [...dates],
//         y: dates.map(()=>Math.random()),
//         meta: dates.map(()=>Math.random()),
//         name: 'PullRequestReviewEvent',
//       },
//       {
//         x: [...dates],
//         y: dates.map(()=>Math.random()),
//         meta: dates.map(()=>Math.random()),
//         name: 'PullRequestEvent',
//       }

// ]

export default {
  title: "Tilde/GithubAcivity",
  component: GithubAcivity,
  // argTypes: {
  //   backgroundColor: { control: 'color' },
  // },
};

const Template = (args) => <GithubAcivity {...args} />;

export const Primary = Template.bind({});
Primary.args = {
  activityLog,
};
