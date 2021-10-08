import React from "react";
import Presentation from "./Presentation";
import { connect } from "react-redux";

import { apiReduxApps } from "../../../../apiAccess/redux/apiApps";

function TeamsTableUnconnected({
  user,
  userId,
  fetchUser,
}) {
  React.useEffect(() => {
    if (userId) {
      fetchUser({ userId });
    }
  }, [
    userId,
    fetchUser,
  ]);

  const props = {
    user,
    userId,
  };

  return <Presentation {...props} />;
}

const mapStateToProps = (state) => {
  const user = state.TeamsTable.user;
  return { user };
}

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

const TeamsTable = connect(
  mapStateToProps,
  mapDispatchToProps
)(TeamsTableUnconnected);

export default TeamsTable;