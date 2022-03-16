import React from "react";

import Reviews from "../components/pages/CardDetails/Reviews";

import reviewObject from "./fixtures/review.json";

export default {
  title: "Tilde/pages/CardDetails/Reviews",
  component: Reviews,
  argTypes: {
    //   backgroundColor: { control: 'color' },
  },
};

const Template = (args) => <Reviews {...args} />;
export const Loading = Template.bind({});
Loading.args = {
  reviewIds: [123],
  reviews: [],
};
export const Primary = Template.bind({});
Primary.args = {
  reviewIds: [4857],
  reviews: [
    {
      id: 4857,
      status: "E",
      timestamp: "2020-10-29T12:47:20.636784Z",
      comments: "This is good work! There are ",
    },
    reviewObject,
    {
      id: 11453,
      status: "C",
      timestamp: "2021-05-20T10:53:11.474581Z",
      comments: "Good work",
      recruitProject: 5434,
      reviewerUser: 296,
      reviewerUserEmail: "sylvester.magwaza@umuzi.org",
      title: "Level 2 coding challenges",
      reviewedUserEmails: ["tumelo.mahlangu@umuzi.org"],
      reviewedUserIds: [696],
      trusted: false,
      validated: "d",
      agileCard: 100529,
    },
    {
      id: 4857,
      status: "C",
      timestamp: "2020-10-29T07:47:20.636784Z",
      comments: "This is good work! There are ",
    },
    {
      id: 10639,
      status: "C",
      timestamp: "2021-05-06T07:08:47.072540Z",
      comments: "Requested changes made: removed comments. Good work",
      recruitProject: 5417,
      reviewerUser: 297,
      reviewerUserEmail: "manelisi.madini@umuzi.org",
      title: "Level 2 coding challenges",
      reviewedUserEmails: ["refilwe.mashile@umuzi.org"],
      reviewedUserIds: [490],
      trusted: false,
      validated: "i",
      agileCard: 99771,
    },
  ],
};
