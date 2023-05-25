import React from "react";

import UserNavBar from "../components/regions/UserNavBar/Presentation";
import { BrowserRouter as Router } from "react-router-dom";

export default {
  title: "Tilde/UserNavBar",
  component: UserNavBar,
  // argTypes: {
  //   backgroundColor: { control: 'color' },
  // },
};

const Template = (args) => (
  <Router>
    <UserNavBar {...args} />
  </Router>
);

export const Primary = Template.bind({});
Primary.args = {
  userId: 1,
  userBoardSelected: true,
  userStatsSelected: false,
  user: {
    email: "sheena.oconnell@umuzi.org",
    githubName: "sheenarbw",
  },
};
