import React from "react";

import activityLogBarGraphStorybookData from "./storyData/activityLogBarGraphStorybookData.json";
import { ActivityDashboardBarGraphUnconnected } from ".";

export default {
  title: "Tilde/pages/userActions/ActivityDashboardBarGraph",
  component: ActivityDashboardBarGraphUnconnected,
};

const Template = (args) => <ActivityDashboardBarGraphUnconnected {...args} />;

export const Primary = Template.bind({});

Primary.args = {
  activityLogDayCounts: activityLogBarGraphStorybookData.activityLogDayCount,
  eventTypes: activityLogBarGraphStorybookData.eventTypes,
};
