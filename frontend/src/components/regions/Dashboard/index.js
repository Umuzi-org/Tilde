import React, { useEffect } from "react";
import Presentation from "./Presentation";
import { connect } from "react-redux";
import { useParams } from "react-router-dom";

function DashboardUnconnected({ user, authedUserId }) {
  let urlParams = useParams() || {};
  const userId = parseInt(urlParams.userId || authedUserId || 0);
  
  return <Presentation />;
}

const mapStateToProps = (state) => {
  return {
    authedUserId: state.App.authUser.userId,

  }
}

const mapDispatchToProps = (dispatch) => {
  return {
    
  }
}

const Dashboard = connect(
  mapStateToProps,
  mapDispatchToProps
)(DashboardUnconnected);

export default Dashboard;