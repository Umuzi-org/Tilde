import React from "react";

import TeamDashboard from "../components/pages/TeamDashboard/Presentation.jsx";
import activityLogDayCounts from "./fixtures/activityLogDayCounts.json";
import team from "./fixtures/team.json";

export default {
  title: "Tilde/pages/TeamDashboard",
  component: TeamDashboard,
  argTypes: {},
};

const Template = (args) => <TeamDashboard {...args} />;

export const Primary = Template.bind({});
Primary.args = {
  team,
  activityLogDayCounts,
};
