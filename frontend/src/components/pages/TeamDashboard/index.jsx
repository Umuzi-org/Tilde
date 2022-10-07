import React, { useEffect } from "react";
import Presentation from "./Presentation.jsx";
import { apiReduxApps } from "../../../apiAccess/apiApps";
import { connect } from "react-redux";
import { useParams } from "react-router-dom";

import Loading from "../../widgets/Loading";

import {
  ACTIVITY_LOG_EVENT_TYPE_COMPETENCE_REVIEW_DONE,
  ACTIVITY_LOG_EVENT_TYPE_PR_REVIEWED,
} from "../../../constants";

import { getActivityLogCountsByDayForUsers } from "../../../apiAccess/selectors/activityLogSelectors";

function DashboardUnconnected({
  teams,
  activityLogDayCounts,
  fetchTeam,
  fetchUserActivityLogDayCountsSequence,
}) {
  let urlParams = useParams() || {};

  const teamId = parseInt(urlParams.teamId, 10);
  const team = teams && teams[teamId];
  activityLogDayCounts = [];

  useEffect(() => {
    if (teamId) {
      fetchTeam({ teamId });
    }

    if (team) {
      const dataSequence = team.members
        .map((member) => [
          {
            eventTypeName: ACTIVITY_LOG_EVENT_TYPE_COMPETENCE_REVIEW_DONE,
            actorUser: member.userId,
            page: 1,
          },
          {
            eventTypeName: ACTIVITY_LOG_EVENT_TYPE_PR_REVIEWED,
            actorUser: member.userId,
            page: 1,
          },
        ])
        .flat();

      fetchUserActivityLogDayCountsSequence({ dataSequence });
    }
  }, [teamId, fetchTeam, team, fetchUserActivityLogDayCountsSequence]);

  if (teams === undefined) return <Loading />;

  const eventTypes = [
    ACTIVITY_LOG_EVENT_TYPE_COMPETENCE_REVIEW_DONE,
    ACTIVITY_LOG_EVENT_TYPE_PR_REVIEWED,
  ];

  const props = {
    team,
    activityLogDayCounts: getActivityLogCountsByDayForUsers({
      activityLogDayCounts,
      eventTypes,
      userIds: team ? team.members.map((member) => member.userId) : [],
    }),
  };

  return <Presentation {...props} />;
}

function mapStateToProps(state) {
  return {
    teams: state.apiEntities.teams,
    authUser: state.App.authUser,
    activityLogDayCounts: state.apiEntities.activityLogDayCounts,
  };
}

function mapDispatchToProps(dispatch) {
  return {
    fetchTeam: function ({ teamId }) {
      dispatch(
        apiReduxApps.FETCH_SINGLE_TEAM.operations.maybeStart({
          data: { teamId: parseInt(teamId) },
        })
      );
    },

    fetchUserActivityLogDayCountsSequence: function ({ dataSequence }) {
      dispatch(
        apiReduxApps.FETCH_ACTIVITY_LOG_DAY_COUNTS_PAGE.operations.maybeStartCallSequence(
          {
            dataSequence,
          }
        )
      );
    },
  };
}

const Dashboard = connect(
  mapStateToProps,
  mapDispatchToProps
)(DashboardUnconnected);

export default Dashboard;
