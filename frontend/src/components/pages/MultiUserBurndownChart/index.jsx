import React from "react";
import Presentation from "./Presentation";
import { connect } from "react-redux";
import { useParams } from "react-router-dom";
// import { apiReduxApps } from "../../../apiAccess/apiApps";

export function MultiUserBurndownChartUnconnected({
  //   mapStateToProps
  currentUserBurndownStats,
  // mapDispatchToProps

  // storybook
  forceUser,
}) {
  let urlParams = useParams() || {};
  const authedUser = forceUser || parseInt(urlParams.userId);
  currentUserBurndownStats = currentUserBurndownStats || {};
  currentUserBurndownStats.map(
    (burnDownSnapshot) =>
      (burnDownSnapshot.timestamp = new Date(burnDownSnapshot.timestamp)
        .toISOString()
        .slice(0, 10))
  );

    // organize data from the team, and format it so the chart can use it
    const usersOnTeam = [];
    currentUserBurndownStats.forEach((snapshot) => {
      if (
        !usersOnTeam.some((user) => user.user === snapshot.user)
      ) {
        const userSnapshot = {
          user: snapshot.user,
          userEmail: snapshot.userEmail,
          snapshot: [snapshot],
        };
        usersOnTeam.push(userSnapshot);
      } else if (usersOnTeam.some((user) => user.user === snapshot.user)) {
        const userIndex = usersOnTeam.findIndex((user) => {
          return user.user === snapshot.user;
        });
        usersOnTeam[userIndex].snapshot.push(snapshot);
      }
    });

  const props = {
    currentUserBurndownStats,
    usersOnTeam,
    authedUser
  }

  return <Presentation {...props} />;
}

const mapStateToProps = (state) => {};

const mapDispatchToProps = (dispatch) => {};

const MultiUserBurndownChart = connect(
  mapStateToProps,
  mapDispatchToProps
)(MultiUserBurndownChartUnconnected);
export default MultiUserBurndownChart;
