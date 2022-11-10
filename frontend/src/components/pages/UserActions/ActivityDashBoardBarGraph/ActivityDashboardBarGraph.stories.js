import React from "react";

import allUserActions from "./storyData/allUserActions.json";
import { ActivityDashboardBarGraphUnconnected } from ".";

export default {
  title: "Tilde/pages/userActions/ActivityDashboardBarGraph",
  component: ActivityDashboardBarGraphUnconnected,
};

const Template = (args) => <ActivityDashboardBarGraphUnconnected {...args} />;

export const Primary = Template.bind({});

Primary.args = {
  activityLogDayCounts: allUserActions.activityLogDayCount,
  eventTypes: allUserActions.eventTypes,
};
