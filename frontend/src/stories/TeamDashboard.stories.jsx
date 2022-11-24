import React from "react";

import TeamDashboard from "../components/pages/TeamDashboard/Presentation.jsx";
import team from "./fixtures/team.json";

const date = (n) => {
  const todayDate = new Date();
  todayDate.setDate(todayDate.getDate() - n);

  const formattedDate = `${todayDate.getFullYear()}-${
    todayDate.getMonth() + 1
  }-${todayDate.getDate()}`;

  return formattedDate;
};

const activityLogDayCounts = {
  84: [
    {
      date: date(7),
      COMPETENCE_REVIEW_DONE: 5,
      PR_REVIEWED: 3,
    },
    {
      date: date(15),
      COMPETENCE_REVIEW_DONE: 6,
      PR_REVIEWED: 20,
    },
    {
      date: date(18),
      COMPETENCE_REVIEW_DONE: 20,
      PR_REVIEWED: 0,
    },
    {
      date: date(11),
      COMPETENCE_REVIEW_DONE: 20,
      PR_REVIEWED: 0,
    },
    {
      date: date(8),
      COMPETENCE_REVIEW_DONE: 20,
      PR_REVIEWED: 0,
    },
    {
      date: date(5),
      COMPETENCE_REVIEW_DONE: 20,
      PR_REVIEWED: 0,
    },
  ],

  26: [
    {
      date: date(18),
      COMPETENCE_REVIEW_DONE: 5,
      PR_REVIEWED: 3,
    },
    {
      date: date(5),
      COMPETENCE_REVIEW_DONE: 6,
      PR_REVIEWED: 2,
    },
    {
      date: date(4),
      COMPETENCE_REVIEW_DONE: 20,
      PR_REVIEWED: 1,
    },
  ],

  132: [
    {
      date: date(2),
      COMPETENCE_REVIEW_DONE: 50,
      PR_REVIEWED: 31,
    },
    {
      date: date(10),
      COMPETENCE_REVIEW_DONE: 20,
      PR_REVIEWED: 12,
    },
    {
      date: date(13),
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
