import React from "react";

import TeamDashboard from "../components/pages/TeamDashboard/Presentation.jsx";
import { filterByStartDate } from "../utils/filterByStartDate.js";
import team from "./fixtures/team.json";

const activityLogDayCounts = {
  84: [
    {
      date: filterByStartDate(17),
      COMPETENCE_REVIEW_DONE: 5,
      PR_REVIEWED: 3,
    },
    {
      date: filterByStartDate(16),
      COMPETENCE_REVIEW_DONE: 6,
      PR_REVIEWED: 20,
    },
    {
      date: filterByStartDate(15),
      COMPETENCE_REVIEW_DONE: 20,
      PR_REVIEWED: 0,
    },
    {
      date: filterByStartDate(14),
      COMPETENCE_REVIEW_DONE: 20,
      PR_REVIEWED: 0,
    },
    {
      date: filterByStartDate(13),
      COMPETENCE_REVIEW_DONE: 20,
      PR_REVIEWED: 0,
    },
    {
      date: filterByStartDate(12),
      COMPETENCE_REVIEW_DONE: 20,
      PR_REVIEWED: 0,
    },
  ],

  26: [
    {
      date: filterByStartDate(17),
      COMPETENCE_REVIEW_DONE: 5,
      PR_REVIEWED: 3,
    },
    {
      date: filterByStartDate(10),
      COMPETENCE_REVIEW_DONE: 6,
      PR_REVIEWED: 2,
    },
    {
      date: filterByStartDate(9),
      COMPETENCE_REVIEW_DONE: 20,
      PR_REVIEWED: 1,
    },
  ],

  132: [
    {
      date: filterByStartDate(8),
      COMPETENCE_REVIEW_DONE: 50,
      PR_REVIEWED: 31,
    },
    {
      date: filterByStartDate(7),
      COMPETENCE_REVIEW_DONE: 20,
      PR_REVIEWED: 12,
    },
    {
      date: filterByStartDate(6),
      COMPETENCE_REVIEW_DONE: 1,
      PR_REVIEWED: 11,
    },
  ],
};

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
