import React from "react";

import ActivityLog from "../components/pages/UserActions/ActivityLog";
import ActivityLogList from "./fixtures/activityLogList.json";
import { MemoryRouter as Router } from "react-router-dom";

const orderedDates = ["2022-09-05", "2022-09-02", "2022-09-01"];

export default {
  title: "Tilde/UserActions/ActivityLog",
  component: ActivityLog,
};
const Template = (args) => (
  <Router>
    <ActivityLog {...args} />
  </Router>
);

export const Primary = Template.bind({});
Primary.args = {
  eventList: ActivityLogList,
  orderedDates,
};
