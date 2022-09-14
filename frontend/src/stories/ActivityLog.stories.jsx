import React from "react";

import ActivityLog from "../components/regions/UserActions/ActivityLog";
import ActivityLogList from "./fixtures/activityLogList.json";

const sortedTimestampArray = [
  "2022-09-05T10:46:16.221191Z",
  "2022-09-02T13:46:16.295020Z",
  "2022-09-01T13:18:03.743668Z",
];

export default {
  title: "Tilde/ActivityLog",
  component: ActivityLog,
};

const Template = (args) => <ActivityLog {...args} />;

export const Primary = Template.bind({});
Primary.args = {
  eventList: ActivityLogList,
  sortedTimestampArray,
};
