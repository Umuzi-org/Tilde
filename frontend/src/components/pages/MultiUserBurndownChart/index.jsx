import React from "react";
import Presentation from "./Presentation";
import { connect } from "react-redux";
import { fillInSnapshotDateGaps } from "./utils";

export function MultiUserBurndownChartUnconnected({
  //   mapStateToProps
  currentTeamBurndownStats,
  team,
  metrics,
  // mapDispatchToProps

  // storybook
}) {
  currentTeamBurndownStats = currentTeamBurndownStats
    ? Object.values(currentTeamBurndownStats)
    : {};
  currentTeamBurndownStats.map(
    (burnDownSnapshot) =>
      (burnDownSnapshot.timestamp = new Date(burnDownSnapshot.timestamp)
        .toISOString()
        .slice(0, 10))
  );
  // organize data from the team, and format it so the chart can use it
  const userSnapshotArray = [];
  currentTeamBurndownStats.forEach((snapshot) => {
    if (!userSnapshotArray.some((user) => user.user === snapshot.user)) {
      let currentUserEmail = '';
      team.members.forEach(member => {
        if(member.userId === snapshot.user){
          currentUserEmail = member.userEmail;
        }
      });
      const userSnapshot = {
        user: snapshot.user,
        userEmail: currentUserEmail,
        snapshot: [snapshot],
      };
      userSnapshotArray.push(userSnapshot);
    } else if (userSnapshotArray.some((user) => user.user === snapshot.user)) {
      const userIndex = userSnapshotArray.findIndex((user) => {
        return user.user === snapshot.user;
      });
      userSnapshotArray[userIndex].snapshot.push(snapshot);
    }
  });

  userSnapshotArray.forEach((user) => {
    const currentUserBurndownStats = user.snapshot;
    const newUserBurndownStats = fillInSnapshotDateGaps({
      currentUserBurndownStats,
    });
    user.snapshot = newUserBurndownStats;
  });

  const props = {
    userSnapshotArray,
    metrics,
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
