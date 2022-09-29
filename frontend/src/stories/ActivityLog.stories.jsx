import React from "react";

import ActivityLog from "../components/regions/UserActions/ActivityLog";
import ActivityLogList from "./fixtures/activityLogList.json";

const sortedTimestampArray = ["2022-09-05", "2022-09-02", "2022-09-01"];

export default {
  title: "Tilde/UserActions/ActivityLog",
  component: ActivityLog,
};

const Template = (args) => <ActivityLog {...args} />;

export const Primary = Template.bind({});
Primary.args = {
  eventList: ActivityLogList,
  sortedTimestampArray,
};
