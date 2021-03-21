import React from "react";

import UserActions from "../components/regions/UserActions/Presentation";
import actionLogByDate from "./fixtures/userActionLogsByDate.json";

const orderedDates = [
  "Sunday 21/03/2021",
  "Thursday 11/03/2021",
  "Monday 08/03/2021",
  "Wednesday 03/03/2021",
  "Tuesday 02/03/2021",
  "Monday 01/03/2021",
];

export default {
  title: "Tilde/UserActions",
  component: UserActions,
  // argTypes: {
  //   backgroundColor: { control: 'color' },
  // },
};

const Template = (args) => <UserActions {...args} />;

export const Primary = Template.bind({});
Primary.args = {
  //   activityLog,
  orderedDates,
  actionLogByDate,
  anyLoading: true,
};
