import React from "react";
import Button from "../components/widgets/Button.jsx";

export default {
  title: "Tilde/Button",
  component: Button,
};
const Template = (args) => <Button {...args}>Button</Button>;

export const Primary = Template.bind({});
Primary.args = {
  button: Button,
};
