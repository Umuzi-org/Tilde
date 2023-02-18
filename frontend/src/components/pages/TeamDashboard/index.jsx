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
  // mapStateToProps
  teams,
  eventTypes,
  activityLogDayCounts,

  // mapDispatchToProps
  fetchTeam,
  fetchUserActivityLogDayCountsSequence,
  fetchEventTypes,
}) {
  let urlParams = useParams() || {};
  const teamId = parseInt(urlParams.teamId, 10);
  const team = teams && teams[teamId];

  const eventTypeNames = [
    // we'll graph these
    ACTIVITY_LOG_EVENT_TYPE_COMPETENCE_REVIEW_DONE,
    ACTIVITY_LOG_EVENT_TYPE_PR_REVIEWED,
  ];

  const eventTypeIds =
    eventTypes &&
    eventTypeNames.map(
      (name) =>
        Object.values(eventTypes).find((element) => element.name === name).id
    );

  activityLogDayCounts = activityLogDayCounts
    ? Object.values(activityLogDayCounts)
    : [];

  useEffect(() => fetchEventTypes(), [fetchEventTypes]);
  useEffect(() => {
    if (teamId) {
      fetchTeam({ teamId });
    }
  }, [fetchTeam, teamId]);

  useEffect(() => {
    if (team && eventTypes) {
      const dataSequence = team.members
        .map((member) =>
          eventTypeIds.map((id) => ({
            eventType: id,
            actorUser: member.userId,
            page: 1,
          }))
        )
        .flat();
      fetchUserActivityLogDayCountsSequence({ dataSequence });
    }
  }, [team, fetchUserActivityLogDayCountsSequence, eventTypes, eventTypeIds]);

  if (teams === undefined) return <Loading />;
  if (eventTypes === undefined) return <Loading />;

  const props = {
    team,
    activityLogDayCounts: getActivityLogCountsByDayForUsers({
      activityLogDayCounts,
      eventTypes: eventTypeIds,
      userIds: team ? team.members.map((member) => member.userId) : [],
    }),
  };

  console.log({ activityLogDayCounts: props.activityLogDayCounts });

  return <Presentation {...props} />;
}

function mapStateToProps(state) {
  return {
    teams: state.apiEntities.teams,
    eventTypes: state.apiEntities.eventTypes,
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

    fetchEventTypes: function () {
      dispatch(
        apiReduxApps.FETCH_EVENT_TYPES.operations.maybeStart({
          data: { page: 1 },
        })
      );
    },
  };
}

const Dashboard = connect(
  mapStateToProps,
  mapDispatchToProps
)(DashboardUnconnected);

export default Dashboard;
