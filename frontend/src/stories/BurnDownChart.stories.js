import React from "react";
import BurnDownChart from "../components/pages/UserDashboard/BurnDownChart";
import burnDownData from "./fixtures/burnDownData.json";
export default {
    title: "Tilde/pages/UserDashboard/BurnDownChart",
    component: BurnDownChart,
}

console.log(burnDownData);

const Template = (args) => <BurnDownChart {...args} />;

export const Primary = Template.bind({});
Primary.args = {
  burnDownData,
};