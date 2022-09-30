import React, { useEffect } from "react";
import Presentation from "./Presentation";
import { apiReduxApps } from "../../../apiAccess/apiApps";
import { connect } from "react-redux";
import { useParams } from "react-router-dom";

import { hasPermissionOnUser } from "../../../utils/permissions";
import { TEAM_PERMISSIONS } from "../../../constants";

import Loading from "../../widgets/Loading";

function DashboardUnconnected({
  authUser,
  users,
  userDetailedStats,
  fetchUser,
  fetchUserDetailedStats,
}) {
  console.log("xxxxxxx");
  let urlParams = useParams() || {};
  const userId = parseInt(urlParams.userId || authUser.userId || 0);
  const user = users && users[userId];
  const currentUserDetailedStats =
    userDetailedStats && userDetailedStats[userId];

  useEffect(() => {
    if (userId) {
      fetchUser({ userId });
      fetchUserDetailedStats({ userId });
    }
  }, [userId, fetchUser, fetchUserDetailedStats]);

  if (users === undefined || userDetailedStats === undefined)
    return <Loading />;

  const showTeamsTable = user
    ? hasPermissionOnUser({ authUser, user, permissions: TEAM_PERMISSIONS })
    : false;

  const props = {
    user,
    currentUserDetailedStats,
    showTeamsTable,
    authUser,
  };

  return <Presentation {...props} />;
}

const mapStateToProps = (state) => {
  return {
    users: state.apiEntities.users,
    userDetailedStats: state.apiEntities.userDetailedStats,
    userBurndownStats: state.apiEntities.burndownSnapshots,
    // authedUserId: state.App.authUser.userId,
    authUser: state.App.authUser,
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
