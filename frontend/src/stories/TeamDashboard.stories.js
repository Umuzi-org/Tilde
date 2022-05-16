import React from "react";

import TeamDashboard from "../components/pages/TeamDashboard/Presentation.jsx";

const team = {
  id: 29,
  name: "Staff Tech Education",
  active: true,
  members: [
    {
      userId: 84,
      userEmail: "siphiwe.mahlangu@umuzi.org",
      userActive: true,
    },
    {
      userId: 26,
      userEmail: "sbonelo.mkhize@umuzi.org",
      userActive: true,
    },
    {
      userId: 132,
      userEmail: "rethabile.thulo@umuzi.org",
      userActive: true,
    },
    {
      userId: 185,
      userEmail: "kaleem.mohammad@umuzi.org",
      userActive: true,
    },
    {
      userId: 228,
      userEmail: "andy.nkumane@umuzi.org",
      userActive: true,
    },
    {
      userId: 274,
      userEmail: "thabile.nhlapo@umuzi.org",
      userActive: true,
    },
    {
      userId: 295,
      userEmail: "babalwa.mbolekwa@umuzi.org",
      userActive: true,
    },
    {
      userId: 700,
      userEmail: "eckard.berry@umuzi.org",
      userActive: true,
    },
    {
      userId: 219,
      userEmail: "faith.mofokeng@umuzi.org",
      userActive: true,
    },
    {
      userId: 891,
      userEmail: "vuyisanani.meteni@umuzi.org",
      userActive: true,
    },
    {
      userId: 890,
      userEmail: "jacob.masinire@umuzi.org",
      userActive: true,
    },
    {
      userId: 231,
      userEmail: "asanda.radebe@umuzi.org",
      userActive: true,
    },
    {
      userId: 236,
      userEmail: "lerato.mabe@umuzi.org",
      userActive: true,
    },
  ],
};

const activityLogDayCounts = {
  84: [
    {
      date: "2020-07-12",
      COMPETENCE_REVIEW_DONE: 5,
      PR_REVIEWED: 3,
    },
    {
      date: "2021-07-16",
      COMPETENCE_REVIEW_DONE: 6,
      PR_REVIEWED: 20,
    },
    {
      date: "2022-02-17",
      COMPETENCE_REVIEW_DONE: 20,
      PR_REVIEWED: 0,
    },
    {
      date: "2022-03-18",
      COMPETENCE_REVIEW_DONE: 20,
      PR_REVIEWED: 0,
    },
    {
      date: "2022-03-19",
      COMPETENCE_REVIEW_DONE: 20,
      PR_REVIEWED: 0,
    },
    {
      date: "2022-03-20",
      COMPETENCE_REVIEW_DONE: 20,
      PR_REVIEWED: 0,
    },
  ],

  26: [
    {
      date: "2021-07-15",
      COMPETENCE_REVIEW_DONE: 5,
      PR_REVIEWED: 3,
    },
    {
      date: "2021-07-10",
      COMPETENCE_REVIEW_DONE: 6,
      PR_REVIEWED: 2,
    },
    {
      date: "2021-07-17",
      COMPETENCE_REVIEW_DONE: 20,
      PR_REVIEWED: 1,
    },
  ],

  132: [
    {
      date: "2021-07-15",
      COMPETENCE_REVIEW_DONE: 50,
      PR_REVIEWED: 3,
    },
    {
      date: "2021-07-16",
      COMPETENCE_REVIEW_DONE: 20,
      PR_REVIEWED: 2,
    },
    {
      date: "2021-07-31",
      COMPETENCE_REVIEW_DONE: 1,
      PR_REVIEWED: 1,
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
