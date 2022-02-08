import React from "react";
import TeamsTable from "../components/regions/UserDetails/TeamsTable/Presentation";
import authUser from "./fixtures/authUser.json";

export default {
    title: "Tilde/UserTeamsTable",
    component: TeamsTable,
}

const Template = args => <TeamsTable {...args} />

export const Primary = Template.bind({});
Primary.args = {
  teams: authUser.teamMemberships,
  authUser: authUser
}
