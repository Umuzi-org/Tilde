import React from "react";

import actionLogByDate from "./fixtures/userActionLogsByDate.json";
import EntryListEndpoint from "../components/widgets/EntryListEndpoint";
import apis from "../apiAccess/apis";

// const orderedDates = [
//   "Sunday 21/03/2021",
//   "Thursday 11/03/2021",
//   "Monday 08/03/2021",
//   "Wednesday 03/03/2021",
//   "Tuesday 02/03/2021",
//   "Monday 01/03/2021",
// ];

export default {
  title: "Tilde/EntryListEndpoint",
  component: EntryListEndpoint,
};

const Template = (args) => <EntryListEndpoint {...args} />;

export const Primary = Template.bind({});
Primary.args = {
  activityLog: apis.activityLogDayCountsPage,
  // orderedDates,
  actionLogByDate,
  anyLoading: true,
};
