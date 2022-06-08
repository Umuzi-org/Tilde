import React from "react";
import Presentation from "./Presentation";
import { apiReduxApps } from "../../../apiAccess/apiApps";
import { connect } from "react-redux";
import { useParams } from "react-router-dom";

import { hasPermissionOnUser } from "../../../utils/permissions";
import { TEAM_PERMISSIONS } from "../../../constants";
import burnDownData from "../../../stories/fixtures/burnDownData.json";

function DashboardUnconnected({
  authUser,
  users,
  userDetailedStats,
  userBurndownStats,
  fetchUser,
  fetchUserDetailedStats,
  fetchUserBurndownStats,
}) {
  let urlParams = useParams() || {};
  const userId = parseInt(urlParams.userId || authUser.userId || 0);
  const user = users[userId];
  const detailedStats = userDetailedStats[userId];
  const burndownStats = burnDownData;

  React.useEffect(() => {
    if (userId) {
      fetchUser({ userId });
      fetchUserDetailedStats({ userId });
      fetchUserBurndownStats({ userId });
    }
  }, [userId, fetchUser, fetchUserDetailedStats, fetchUserBurndownStats]);

  const showTeamsTable = user
    ? hasPermissionOnUser({ authUser, user, permissions: TEAM_PERMISSIONS })
    : false;

  const props = {
    user,
    detailedStats,
    burndownStats,
    showTeamsTable,
    authUser,
  };

  return <Presentation {...props} />;
}

const mapStateToProps = (state) => {
  return {
    users: state.apiEntities.users || {},
    userDetailedStats: state.apiEntities.userDetailedStats || {},
    fetchUserBurndownStats: state.apiEntities.userBurndownStats || {},
    // authedUserId: state.App.authUser.userId,
    authUser: state.App.authUser || {},
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    fetchUser: ({ userId }) => {
      dispatch(
        apiReduxApps.FETCH_SINGLE_USER.operations.maybeStart({
          data: { userId: parseInt(userId) },
        })
      );
    },

    fetchUserDetailedStats: ({ userId }) => {
      dispatch(
        apiReduxApps.FETCH_SINGLE_USER_DETAILED_STATS.operations.maybeStart({
          data: { userId: parseInt(userId) },
        })
      );
    },
    fetchUserBurndownStats: ({ userId }) => {
      dispatch(
        apiReduxApps.FETCH_USER_BURNDOWN_SNAPSHOTS_PAGE.operations.maybeStart({
          data: { userId: parseInt(userId) },
        })
      );
    },
  };
};

const Dashboard = connect(
  mapStateToProps,
  mapDispatchToProps
)(DashboardUnconnected);

export default Dashboard;
