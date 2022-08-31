import React from "react";
import UserProfile from "../components/pages/UserProfile/Presentation";

export default {
  title: "Tilde/Pages/UserProfile",
  component: UserProfile,
};

export const Primary = (args) => <UserProfile {...args} />;
Primary.args = {
  nameTag: "Some name",
};
