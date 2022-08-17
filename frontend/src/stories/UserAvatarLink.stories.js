import React from "react";
import { BrowserRouter as Router } from "react-router-dom";
import UserAvatarLink from "../components/widgets/UserAvatarLink.jsx";

export default {
  title: "Tilde/UserAvatarLink",
  component: UserAvatarLink,
};

const Template = (args) => (
  <Router>
    <UserAvatarLink {...args} />
  </Router>
);

export const Default = Template.bind({});

Default.args = {
  email: "ngoako.ramokgopa@umuzi.org",
  userId: 5,
};
