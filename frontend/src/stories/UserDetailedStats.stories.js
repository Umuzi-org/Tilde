import React from "react";
import UserDetailedStats from "../components/pages/UserDashboard/UserDetailedStats";
import detailedStats from "./fixtures/userDetailedStats.json";

export default {
  title: "Tilde/UserDashboard/UserDetailedStats",
  component: UserDetailedStats,
  // argTypes: {
  //   backgroundColor: { control: 'color' },
  // },
};

const Template = (args) => <UserDetailedStats {...args} />;

export const Primary = Template.bind({});
Primary.args = {
  detailedStats,
};
