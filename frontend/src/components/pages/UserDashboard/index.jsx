import React from "react";
import Presentation from "./Presentation";
import { apiReduxApps } from "../../../apiAccess/apiApps";
import { connect } from "react-redux";
import { useParams } from "react-router-dom";

import { hasPermissionOnUser } from "../../../utils/permissions";
import { useTraceUpdate } from "../../../hooks"
import { TEAM_PERMISSIONS } from "../../../constants";

function DashboardUnconnected({
  authUser,
  users,
  userDetailedStats,
  userBurndownStats,
  fetchUser,
  fetchUserDetailedStats,
  fetchUserBurndownStats,
}) {
  useTraceUpdate({
    authUser,
    users,
    userDetailedStats,
    userBurndownStats,
    fetchUser,
    fetchUserDetailedStats,
    fetchUserBurndownStats,
  });
  // console.log("xxxxxxx");

  let urlParams = useParams() || {};
  const userId = parseInt(urlParams.userId || authUser.userId || 0);
  const user = users[userId];
  const currentUserDetailedStats = userDetailedStats[userId];
  const currentUserBurndownStats = Object.values(userBurndownStats).filter(
    (snapshot) => snapshot.user === userId
  );

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
    currentUserDetailedStats,
    currentUserBurndownStats,
    showTeamsTable,
    authUser,
  };

  return <Presentation {...props} />;
}

const mapStateToProps = (state) => {
  return {
    users: state.apiEntities.users || {},
    userDetailedStats: state.apiEntities.userDetailedStats || {},
    userBurndownStats: state.apiEntities.burndownSnapshots || {},
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
    //TODO Implement Page check
    fetchUserBurndownStats: ({ userId }) => {
      dispatch(
        apiReduxApps.FETCH_USER_BURNDOWN_SNAPSHOTS_PAGE.operations.maybeStart({
          data: {
            userId: parseInt(userId),
            page: 1,
          },
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
