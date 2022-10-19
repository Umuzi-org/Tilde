import React from "react";

import TeamDashboard from "../components/pages/TeamDashboard/Presentation.jsx";
import { randomDateBetweenCurrentDayAnd21DaysAgo } from "../utils/randomDateBetweenCurrentDayAnd21DaysAgo.js";
import team from "./fixtures/team.json";

const activityLogDayCounts = {
  84: [
    {
      date: randomDateBetweenCurrentDayAnd21DaysAgo(),
      COMPETENCE_REVIEW_DONE: 5,
      PR_REVIEWED: 3,
    },
    {
      date: randomDateBetweenCurrentDayAnd21DaysAgo(),
      COMPETENCE_REVIEW_DONE: 6,
      PR_REVIEWED: 20,
    },
    {
      date: randomDateBetweenCurrentDayAnd21DaysAgo(),
      COMPETENCE_REVIEW_DONE: 20,
      PR_REVIEWED: 0,
    },
    {
      date: randomDateBetweenCurrentDayAnd21DaysAgo(),
      COMPETENCE_REVIEW_DONE: 20,
      PR_REVIEWED: 0,
    },
    {
      date: randomDateBetweenCurrentDayAnd21DaysAgo(),
      COMPETENCE_REVIEW_DONE: 20,
      PR_REVIEWED: 0,
    },
    {
      date: randomDateBetweenCurrentDayAnd21DaysAgo(),
      COMPETENCE_REVIEW_DONE: 20,
      PR_REVIEWED: 0,
    },
  ],

  26: [
    {
      date: randomDateBetweenCurrentDayAnd21DaysAgo(),
      COMPETENCE_REVIEW_DONE: 5,
      PR_REVIEWED: 3,
    },
    {
      date: randomDateBetweenCurrentDayAnd21DaysAgo(),
      COMPETENCE_REVIEW_DONE: 6,
      PR_REVIEWED: 2,
    },
    {
      date: randomDateBetweenCurrentDayAnd21DaysAgo(),
      COMPETENCE_REVIEW_DONE: 20,
      PR_REVIEWED: 1,
    },
  ],

  132: [
    {
      date: randomDateBetweenCurrentDayAnd21DaysAgo(),
      COMPETENCE_REVIEW_DONE: 50,
      PR_REVIEWED: 31,
    },
    {
      date: randomDateBetweenCurrentDayAnd21DaysAgo(),
      COMPETENCE_REVIEW_DONE: 20,
      PR_REVIEWED: 12,
    },
    {
      date: randomDateBetweenCurrentDayAnd21DaysAgo(),
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
