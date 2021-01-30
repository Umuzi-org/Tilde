import React from "react";
import Presentation from "./Presentation";
import { useParams } from "react-router-dom";
import { connect } from "react-redux";
import { apiReduxApps } from "../../../apiAccess/redux/apiApps";

const UserNavBarUnconnected = ({ fetchUser, users, authUserId }) => {
  let urlParams = useParams() || {};

  const userId = urlParams.userId;
  const user = users[userId];
  const authUser = users[authUserId];

  React.useEffect(() => {
    if (!authUser) return;
    if ((userId !== 0) & !user) fetchUser({ userId });
  }, [fetchUser, user, userId, authUser]);

  const url = window.location.href;
  const props = {
    // userId,
    user,
    userBoardSelected: url.endsWith("board"), // these match the urls in routes.js
    UserActionsSelected: url.endsWith("actions"),
  };

  return <Presentation {...props} />;
};

const mapDispatchToProps = (dispatch) => {
  return {
    fetchUser: ({ userId }) => {
      dispatch(
        apiReduxApps.FETCH_SINGLE_USER.operations.maybeStart({
          data: { userId },
        })
      );
    },
  };
};

const mapStateToProps = (state) => {
  return {
    users: state.Entities.users || {},
    authUserId: state.App.authUser.userId,
  };
};

const UserNavBar = connect(
  mapStateToProps,
  mapDispatchToProps
)(UserNavBarUnconnected);

export default UserNavBar;
