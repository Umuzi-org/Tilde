import React from "react";
import Presentation from "./Presentation";
import { apiReduxApps } from "../../../apiAccess/redux/apiApps";
import { connect } from "react-redux";
import { useParams } from "react-router-dom";

function DashboardUnconnected({ users, authedUserId, fetchUser }) {
  let urlParams = useParams() || {};
  const userId = parseInt(urlParams.userId || authedUserId || 0);
  const user = users[userId];
  React.useEffect(() => {
    if(userId) {
      fetchUser({ userId })
    }
}, [
    userId,
    fetchUser,
    user,
]);

  const props = {
    user,
  }

  return <Presentation {...props} />;
}

const mapStateToProps = (state) => {
  return {
    users: state.Entities.users || {},
    authedUserId: state.App.authUser.userId,
  }
}

const mapDispatchToProps = (dispatch) => {
  return {
    fetchUser: ({ userId }) => {
      dispatch(
        apiReduxApps.FETCH_SINGLE_USER.operations.maybeStart({
          data: { userId: parseInt(userId) },
        })
      );
    },
  }
}

const Dashboard = connect(
  mapStateToProps,
  mapDispatchToProps
)(DashboardUnconnected);

export default Dashboard;