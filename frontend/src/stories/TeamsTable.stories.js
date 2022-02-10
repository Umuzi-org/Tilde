import React from "react";
import TeamsTable from "../components/regions/UserDetails/TeamsTable/Presentation";
import authUser from "./fixtures/authUser.json";
import user from "./fixtures/user.json";
import { BrowserRouter as Router } from "react-router-dom";

export default {
    title: "Tilde/UserTeamsTable",
    component: TeamsTable,
}

const Template = args => <Router><TeamsTable {...args} /></Router>

export const Primary = Template.bind({});
Primary.args = {
  teams: user.teamMemberships,
  authUser
}

