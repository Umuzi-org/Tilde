import React from "react";
import Presentation from "./Presentation";
import { useParams } from "react-router-dom";
import { connect } from "react-redux";
import { apiReduxApps } from "../../../apiAccess/apiApps";

const TeamNavBarUnconnected = ({ fetchTeam, teams, authUserId }) => {
  let urlParams = useParams() || {};

  const teamId = urlParams.teamId;
  teams = teams || {};
  const team = teams[teamId];
  const authUser = teams[authUserId];

  React.useEffect(() => {
    if (!authUser) return;
    if ((teamId !== 0) & !team) fetchTeam({ teamId });
  }, [fetchTeam, team, teamId, authUser]);

  const url = window.location.href;
  const teamCardSummarySelected = url.endsWith("/card_summary"); // these match the urls in routes.js. Also the UserNavBar, could definately be more DRY
  const teamDashboardSelected = url.endsWith("/dashboard");

  let selectedTab;
  if (teamCardSummarySelected) {
    selectedTab = 1;
  }
  if (teamDashboardSelected) {
    selectedTab = 0;
  }

  const props = {
    teamId,
    team,
    selectedTab,
  };

  return <Presentation {...props} />;
};

const mapDispatchToProps = (dispatch) => {
  return {
    fetchTeam: ({ teamId }) => {
      dispatch(
        apiReduxApps.FETCH_SINGLE_TEAM.operations.maybeStart({
          data: { teamId: parseInt(teamId) },
        })
      );
    },
  };
};

const mapStateToProps = (state) => {
  return {
    teams: state.apiEntities.teams,
    authteamId: state.App.authUser.teamId,
  };
};

const TeamNavBar = connect(
  mapStateToProps,
  mapDispatchToProps
)(TeamNavBarUnconnected);

export default TeamNavBar;
