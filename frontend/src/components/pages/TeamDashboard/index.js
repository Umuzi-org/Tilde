import React from "react";
import Presentation from "./Presentation";
import { apiReduxApps } from "../../../apiAccess/apiApps";
import { connect } from "react-redux";
import { useParams } from "react-router-dom";

import {
  ACTIVITY_LOG_EVENT_TYPE_COMPETENCE_REVIEW_DONE,
  ACTIVITY_LOG_EVENT_TYPE_PR_REVIEWED,
} from "../../../constants";

import { getActivityLogCountsByDayForUsers } from "../../../apiAccess/selectors/activityLogSelectors";

import { getMinAndMaxDate } from "./utils";

function DashboardUnconnected({
  // authUser,
  teams,
  activityLogDayCounts,
  fetchTeam,
  fetchUserActivityLogDayCountsSequence,
}) {
  let urlParams = useParams() || {};

  const teamId = parseInt(urlParams.teamId, 10);
  const team = teams[teamId];
  //   const detailedStats = userDetailedStats[userId];

  React.useEffect(() => {
    if (teamId) {
      fetchTeam({ teamId });
      //   fetchTeamDetailedStats({ userId });
    }

    if (team) {
      const dataSequence = team.members
        .map((member) => [
          {
            eventTypeName: ACTIVITY_LOG_EVENT_TYPE_COMPETENCE_REVIEW_DONE,
            actorUser: member.userId,
            // effectedUser,
            page: 1,
          },
          {
            eventTypeName: ACTIVITY_LOG_EVENT_TYPE_PR_REVIEWED,
            actorUser: member.userId,
            // effectedUser,
            page: 1,
          },
        ])
        .flat();

      fetchUserActivityLogDayCountsSequence({ dataSequence });
    }
  }, [teamId, fetchTeam, team, fetchUserActivityLogDayCountsSequence]);

  //   const showTeamsTable = user
  //     ? hasPermissionOnUser({ authUser, user, permissions: TEAM_PERMISSIONS })
  //     : false;

  // console.log(activityLogDayCounts);
  const eventTypes = [
    ACTIVITY_LOG_EVENT_TYPE_COMPETENCE_REVIEW_DONE,
    ACTIVITY_LOG_EVENT_TYPE_PR_REVIEWED,
  ];
  const { minimumDate, maximumDate } = getMinAndMaxDate({
    activityLogDayCounts,
  });

  const props = {
    team,
    activityLogDayCounts: getActivityLogCountsByDayForUsers({
      activityLogDayCounts,
      eventTypes,
      userIds: team ? team.members.map((member) => member.userId) : [],
    }),
    minimumDate,
    maximumDate,
  };

  return <Presentation {...props} />;
}

const mapStateToProps = (state) => {
  return {
    // users: state.apiEntities.users || {},
    teams: state.apiEntities.teams || {},
    // userDetailedStats: state.apiEntities.userDetailedStats || {},
    // authedUserId: state.App.authUser.userId,
    authUser: state.App.authUser || {},

    activityLogDayCounts: Object.values(
      state.apiEntities.activityLogDayCounts || {}
    ),
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    fetchTeam: ({ teamId }) => {
      dispatch(
        apiReduxApps.FETCH_SINGLE_TEAM.operations.maybeStart({
          data: { teamId: parseInt(teamId) },
        })
      );
    },

    fetchUserActivityLogDayCountsSequence: ({ dataSequence }) => {
      dispatch(
        apiReduxApps.FETCH_ACTIVITY_LOG_DAY_COUNTS_PAGE.operations.maybeStartCallSequence(
          {
            dataSequence,
          }
        )
      );
    },

    // fetchTeamDetailedStats: ({ userId }) => {
    //   dispatch(
    //     apiReduxApps.FETCH_SINGLE_USER_DETAILED_STATS.operations.maybeStart({
    //       data: { userId: parseInt(userId) },
    //     })
    //   );
    // },
  };
};

const Dashboard = connect(
  mapStateToProps,
  mapDispatchToProps
)(DashboardUnconnected);

export default Dashboard;
