import React from "react";

import TeamDashboard from "../components/pages/TeamDashboard/Presentation";

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

export default {
  title: "Tilde/pages/TeamDashboard",
  component: TeamDashboard,
  argTypes: {
    //   backgroundColor: { control: 'color' },
  },
};

const Template = (args) => <TeamDashboard {...args} />;

export const Primary = Template.bind({});
Primary.args = {
  team,
};
