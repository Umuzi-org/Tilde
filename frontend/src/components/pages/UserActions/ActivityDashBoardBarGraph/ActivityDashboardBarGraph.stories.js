import React from "react";

import activityBarGraphData from "./storyData/ActivityDashBoardBargraphData.json";
import eventTypeData from "./storyData/eventTypes.json";
import { ActivityDashboardBarGraphUnconnected } from ".";

export default {
  title: "Tilde/pages/userActions/ActivityDashboardBarGraph",
  component: ActivityDashboardBarGraphUnconnected,
};

const Template = (args) => <ActivityDashboardBarGraphUnconnected {...args} />;

export const Primary = Template.bind({});

Primary.args = {
  activityLogDayCounts: activityBarGraphData,
  eventTypes: eventTypeData,
};
