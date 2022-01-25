import React from "react";
import TeamsTable from "../components/regions/UserDetails/TeamsTable/Presentation";
import user from "./fixtures/user.json";

export default {
    title: "Tilde/UserTeamsTable",
    component: TeamsTable,
}

const Template = args => <TeamsTable {...args} />

export const Primary = Template.bind({});
Primary.args = {
  teams: user.teamMemberships,
  authUser: user
}
