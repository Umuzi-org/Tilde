import React from "react";
import Presentation from "./Presentation";
import { apiReduxApps } from "../../../apiAccess/apiApps";
import { connect } from "react-redux";
import { useParams } from "react-router-dom";

// import { hasPermissionOnUser } from "../../../utils/permissions";
// import { TEAM_PERMISSIONS } from "../../../constants";

function DashboardUnconnected({
  authUser,
  teams,
  //   userDetailedStats,
  fetchTeam,
  //   fetchTeamDetailedStats,
}) {
  let urlParams = useParams() || {};

  const teamId = parseInt(urlParams.teamId, 10);
  const team = teams[teamId];
  console.log(team);
  //   const detailedStats = userDetailedStats[userId];

  React.useEffect(() => {
    if (teamId) {
      fetchTeam({ teamId });
      //   fetchTeamDetailedStats({ userId });
    }
  }, [teamId, fetchTeam]);

  //   const showTeamsTable = user
  //     ? hasPermissionOnUser({ authUser, user, permissions: TEAM_PERMISSIONS })
  //     : false;

  const props = {
    // user,
    // detailedStats,
    // showTeamsTable,
    // authUser,
    team,
  };

  return <Presentation {...props} />;
}

const mapStateToProps = (state) => {
  return {
    // users: state.apiEntities.users || {},
    teams: state.apiEntities.teams || {},
    // userDetailedStats: state.apiEntities.userDetailedStats || {},
    // authedUserId: state.App.authUser.userId,
    authUser: state.App.authUser || {},
  };
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

    // fetchTeamDetailedStats: ({ userId }) => {
    //   dispatch(
    //     apiReduxApps.FETCH_SINGLE_USER_DETAILED_STATS.operations.maybeStart({
    //       data: { userId: parseInt(userId) },
    //     })
    //   );
    // },
  };
};

const Dashboard = connect(
  mapStateToProps,
  mapDispatchToProps
)(DashboardUnconnected);

export default Dashboard;
