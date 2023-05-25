import React from "react";
import Typography from "@material-ui/core/Typography";
import EntityNavBar from "../../widgets/EntityNavBar";
import { routes } from "../../../routes";

export default function Presentation({ team, selectedTab, teamId }) {
  const toolbarContents = (
    <React.Fragment>
      {team && <Typography>{team.name}</Typography>}
    </React.Fragment>
  );

  const tabs = [
    // {
    //   to: routes.teamDashboard.route.path.replace(":teamId", teamId),
    //   label: "Dashboard",
    // },
    {
      to: routes.groupCardSummary.route.path.replace(":teamId", teamId),
      label: "Card Summary",
    },
  ];

  return (
    <EntityNavBar
      toolbarContents={toolbarContents}
      tabs={tabs}
      selectedTab={selectedTab}
    />
  );
}
