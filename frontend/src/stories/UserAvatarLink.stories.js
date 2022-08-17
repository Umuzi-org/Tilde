import React from "react";
import UserAvatarLink from "../components/widgets/UserAvatarLink.jsx";

export default {
  title: "Tilde/UserAvatarLink",
  component: UserAvatarLink,
};
const Template = (args) => <UserAvatarLink {...args} />;

export const Default = Template.bind({});
Default.args = {
  email: "ngoako.ramokgopa@umuzi.org",
  userId: 5,
};
