import React from "react";
import Presentation from "./Presentation";
import { connect } from "react-redux";
// import { apiReduxApps } from "../../../apiAccess/redux";

function DashboardUnconnected({ authUser }) {
  return <Presentation />;
}

const mapStateToProps = (state) => {
  return {
    authUser: state.App.authUser,
    // whoAmICallStatus: state.WHO_AM_I,
  };
};

const mapDispatchToProps = (dispatch) => {
  //   const whoAmIStart = (data) => {
  //     dispatch(apiReduxApps.FETCH_RECRUIT_PROJECTS_PAGE.operations.start(data));
  //   };

  //   return { whoAmIStart };
  return {};
};

const Dashboard = connect(
  mapStateToProps,
  mapDispatchToProps
)(DashboardUnconnected);

export default Dashboard;
