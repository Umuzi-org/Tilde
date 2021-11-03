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
