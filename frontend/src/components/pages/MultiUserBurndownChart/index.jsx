import React from "react";
import Presentation from "./Presentation";
import { connect } from "react-redux";
import { useParams } from "react-router-dom";
// import { apiReduxApps } from "../../../apiAccess/apiApps";

export function MultiUserBurndownChartUnconnected({
  //   mapStateToProps
  currentUserBurndownStats,
  userTeam,
  // mapDispatchToProps

  // storybook
  forceUser,
}) {
  let urlParams = useParams() || {};
  const authedUser = forceUser || parseInt(urlParams.userId);
  currentUserBurndownStats = currentUserBurndownStats
    ? Object.values(currentUserBurndownStats)
    : {};
  currentUserBurndownStats.map(
    (burnDownSnapshot) =>
      (burnDownSnapshot.timestamp = new Date(burnDownSnapshot.timestamp)
        .toISOString()
        .slice(0, 10))
  );
  // organize data from the team, and format it so the chart can use it
  const usersOnTeam = [];
  currentUserBurndownStats.forEach((snapshot) => {
    if (!usersOnTeam.some((user) => user.user === snapshot.user)) {
      let currentUserEmail = '';
      userTeam.members.forEach(member => {
        if(member.userId === snapshot.user){
          currentUserEmail = member.userEmail;
        }
      });
      const userSnapshot = {
        user: snapshot.user,
        userEmail: currentUserEmail,
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

  usersOnTeam.forEach((user) => {
    user.snapshot.sort(function(a,b){
      return new Date(a.timestamp) - new Date(b.timestamp);
    });
  });


  const props = {
    usersOnTeam,
    authedUser,
  };

  return <Presentation {...props} />;
}

const mapStateToProps = (state) => {};

const mapDispatchToProps = (dispatch) => {};

const MultiUserBurndownChart = connect(
  mapStateToProps,
  mapDispatchToProps
)(MultiUserBurndownChartUnconnected);
export default MultiUserBurndownChart;
