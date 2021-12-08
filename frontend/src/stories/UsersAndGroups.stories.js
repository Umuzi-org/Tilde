import React from "react";
import UsersAndGroups from "../components/regions/UsersAndGroups/Presentation";
import { BrowserRouter as Router } from "react-router-dom";

import teams from "./fixtures/allTeams.json";
import users from "./fixtures/allUsers.json";

export default {
  title: "Tilde/UsersAndGroups",
  component: UsersAndGroups,
};

const Template = (args) => (
  <Router>
    <UsersAndGroups {...args} />
  </Router>
);

export const Primary = Template.bind({});

Primary.args = {
  teams: teams,
  teamSummaryStats: {
    1: {
      id: 1,
      name: "team1",
      oldestOpenPrTime: "2021-12-06T04:45:01Z",
      totalOpenPrs: 9,
      oldestCardInReviewTime: "2021-12-06T08:23:03.06Z",
      totalCardsInReview: 17,
    },
    2: {
      id: 1,
      name: "team2",
      oldestOpenPrTime: "2021-12-03T04:45:01Z",
      totalOpenPrs: 9,
      oldestCardInReviewTime: "2021-11-06T08:23:03.06Z",
      totalCardsInReview: 17,
    },
  },
  users: users,
  filterByGroup: {
    value: "",
    error: null,
    helpertext: "",
    required: false,
  },
  filterUsersByGroupName: "",
  filterByUser: {
    value: "",
    error: null,
    helpertext: "",
    required: false,
  },

  handleUserGroupClick: () => {},
};
