import React from "react";

import ActivityDashboardBarGraph from "../components/pages/UserActions/ActivityDashboardBarGraph";
import graphData from "./fixtures/ActivityDashBoardBargraphData.json";

export default {
  title: "Tilde/UserActions/ActivityDashboardBarGraph",
  components: ActivityDashboardBarGraph,
  args: {},
};

const Template = (args) => <ActivityDashboardBarGraph {...args} />;

export const Primary = Template.bind({});

Primary.args = {
  eventList: graphData,
};
