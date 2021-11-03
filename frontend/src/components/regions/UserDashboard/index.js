import React from "react";
import Presentation from "./Presentation";
import { apiReduxApps } from "../../../apiAccess/redux/apiApps";
import { connect } from "react-redux";
import { useParams } from "react-router-dom";

function DashboardUnconnected({
  authedUserId,
  users,
  userDetailedStats,
  fetchUser,
  fetchUserDetailedStats,
}) {
  let urlParams = useParams() || {};
  const userId = parseInt(urlParams.userId || authedUserId || 0);
  const user = users[userId];
  const detailedStats = userDetailedStats[userId];

  React.useEffect(() => {
    if (userId) {
      fetchUser({ userId });
      console.log("here");
      fetchUserDetailedStats({ userId });
    }
  }, [userId, fetchUser, fetchUserDetailedStats]);

  const props = {
    user,
    detailedStats,
  };

  return <Presentation {...props} />;
}

const mapStateToProps = (state) => {
  return {
    users: state.Entities.users || {},
    userDetailedStats: state.Entities.userDetailedStats || {},
    authedUserId: state.App.authUser.userId,
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
