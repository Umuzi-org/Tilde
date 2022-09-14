import React from "react";

import ActivityLog from "../components/regions/ActivityLog/Presentation";
import ActivityLogList from "./fixtures/activityLogList.json";

export default {
  title: "Tilde/ActivityLog",
  component: ActivityLog,
};

const Template = (args) => <ActivityLog {...args} />;

export const Primary = Template.bind({});
Primary.args = {
  eventList: ActivityLogList,
};
