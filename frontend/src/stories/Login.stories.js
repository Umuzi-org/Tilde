import React from "react";
import LoginForm from "../components/pages/Login/Presentation";

export default {
  title: "Tilde/Login",
  component: LoginForm,
};

export const Primary = (args) => <LoginForm {...args} />;
Primary.args = {
  loading: false,
  error: "",
  handleLoginWithGoogle: () => {},
};
