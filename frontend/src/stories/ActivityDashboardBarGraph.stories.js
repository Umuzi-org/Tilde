import React from "react";

import ActivityDashboardBarGraph from "../components/regions/UserActions/ActivityDashboardBarGraph";

export default {
  title: "Tilde/regions/UserDashboard/ActivityDashboardBarGraph",
  components: ActivityDashboardBarGraph,
  args: {},
};

const Template = (args) => <ActivityDashboardBarGraph {...args} />;

export const Primary = Template.bind({});
Primary.args = {

};
