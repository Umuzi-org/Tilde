import React from "react";

import allActivityData from "./storyData/allActivityData.json";

import { ActivityDashboardBarGraphUnconnected } from ".";

export default {
  title: "Tilde/pages/userActions/ActivityDashboardBarGraph",
  component: ActivityDashboardBarGraphUnconnected,
};

const Template = (args) => <ActivityDashboardBarGraphUnconnected {...args} />;

export const Primary = Template.bind({});

Primary.args = {
  activityLogDayCounts: allActivityData.activityLogDayCounts,
  eventTypes: allActivityData.eventTypes,
};
