import React from "react";
import UserDetailedStats from "../components/pages/UserDashboard/UserDetailedStats";
import detailedStats from "./fixtures/userDetailedStats.json";

export default {
  title: "Tilde/pages/UserDashboard/UserDetailedStats",
  component: UserDetailedStats,
};

const Template = (args) => <UserDetailedStats {...args} />;

export const Primary = Template.bind({});
Primary.args = {
  detailedStats,
};
