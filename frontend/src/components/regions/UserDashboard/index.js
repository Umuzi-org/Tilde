import React from "react";
import Presentation from "./Presentation";
import { apiReduxApps } from "../../../apiAccess/apiApps";
import { connect } from "react-redux";
import { useParams } from "react-router-dom";

import { hasPermissionOnUser } from "../../../utils/permissions";
import { TEAM_PERMISSIONS } from "../../../constants";

function DashboardUnconnected({
  authUser,
  users,
  userDetailedStats,
  fetchUser,
  fetchUserDetailedStats,
}) {
  let urlParams = useParams() || {};
  const userId = parseInt(urlParams.userId || authUser.userId || 0);
  const user = users[userId];
  const detailedStats = userDetailedStats[userId];

  React.useEffect(() => {
    if (userId) {
      fetchUser({ userId });
      fetchUserDetailedStats({ userId });
    }
  }, [userId, fetchUser, fetchUserDetailedStats]);

  const showTeamsTable = user
    ? hasPermissionOnUser({ authUser, user, permissions: TEAM_PERMISSIONS })
    : false;

  const props = {
    user,
    detailedStats,
    showTeamsTable,
    authUser,
  };

  return <Presentation {...props} />;
}

const mapStateToProps = (state) => {
  return {
    users: state.apiEntities.users || {},
    userDetailedStats: state.apiEntities.userDetailedStats || {},
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
  };
};

const Dashboard = connect(
  mapStateToProps,
  mapDispatchToProps
)(DashboardUnconnected);

export default Dashboard;
