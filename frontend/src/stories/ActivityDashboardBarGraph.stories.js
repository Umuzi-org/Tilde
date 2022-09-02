import React from "react";

import ActivityDashboardBarGraph from "../components/pages/UserDashboard/ActivityDashboardBarGraph";

export default {
  title: "Tilde/pages/UserDashboard/ActivityDashboardBarGraph",
  components: ActivityDashboardBarGraph,
  args: {},
};

const Template = (args) => <ActivityDashboardBarGraph {...args} />;

export const Primary = Template.bind({});
Primary.args = {

};
