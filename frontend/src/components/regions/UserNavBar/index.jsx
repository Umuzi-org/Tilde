import React, { useEffect } from "react";
import Presentation from "./Presentation";
import { useParams } from "react-router-dom";
import { connect } from "react-redux";
import { apiReduxApps } from "../../../apiAccess/apiApps";

// TODO: refactor this. Rather make use of EntityNavBar.
// look at how the team nav bar works

function UserNavBarUnconnected({ fetchUser, users, authUserId }) {
  let urlParams = useParams() || {};

  const userId = urlParams.userId;
  users = users || {};
  const user = users[userId];
  const authUser = users[authUserId];

  useEffect(() => {
    if (!authUser) return;
    if ((userId !== 0) & !user) fetchUser({ userId });
  }, [fetchUser, user, userId, authUser]);

  const url = window.location.href;

  const userBoardSelected = url.endsWith("/board"); // these match the urls in routes.js. Could be more DRY
  const userActionsSelected = url.endsWith("/actions");
  const userDashboardSelected = url.endsWith("/dashboard");

  let value;
  if (userBoardSelected) {
    value = 0;
  }
  if (userActionsSelected) {
    value = 1;
  }
  if (userDashboardSelected) {
    value = 2;
  }
  const props = {
    userId,
    user,
    value,
  };

  return <Presentation {...props} />;
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
  };
};

const mapStateToProps = (state) => {
  return {
    users: state.apiEntities.users,
    authUserId: state.App.authUser.userId,
  };
};

const UserNavBar = connect(
  mapStateToProps,
  mapDispatchToProps
)(UserNavBarUnconnected);

export default UserNavBar;
