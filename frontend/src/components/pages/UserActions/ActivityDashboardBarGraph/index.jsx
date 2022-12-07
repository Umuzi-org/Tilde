import React from "react";
import Presentation from "./Presentation";

import { connect } from "react-redux";
import { useParams } from "react-router-dom";

import { eventTypeColors } from "../../../../colors";
import { prepareDataForBarGraph } from "./utils";
import { apiReduxApps } from "../../../../apiAccess/apiApps";
import { useEffect } from "react";

export function ActivityDashboardBarGraphUnconnected({
  eventTypes,
  activityLogDayCounts,
  fetchEventTypes,
  fetchActivityLogDayCountsPage,
}) {
  const { userId } = useParams() || {};
  eventTypes = eventTypes || {};
  activityLogDayCounts = activityLogDayCounts || {};

  useEffect(() => {
    fetchEventTypes({
      page: 1,
    });
  }, [fetchEventTypes]);

  useEffect(() => {
    fetchActivityLogDayCountsPage({
      actorUser: userId,
      page: 1,
    });
  }, [fetchActivityLogDayCountsPage, userId]);

  const barGraphData = prepareDataForBarGraph({
    eventTypes,
    activityLogDayCounts,
  });

  const colors = Object.entries(eventTypeColors);
  for (const color in colors) {
    for (const event in eventTypes) {
      if (eventTypes[event].name === colors[color][0]) {
        eventTypes[event].color = colors[color][1];
      }
    }
  }

  const props = {
    barGraphData,
    eventTypes: Object.values(eventTypes),
  };

  return <Presentation {...props} />;
}

const mapStateToProps = (state) => {
  return {
    eventTypes: state.apiEntities.eventTypes,
    activityLogDayCounts: state.apiEntities.activityLogDayCounts,
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    fetchEventTypes: () => {
      dispatch(
        apiReduxApps.FETCH_EVENT_TYPES.operations.start({
          data: { page: 1 },
        })
      );
    },
    fetchActivityLogDayCountsPage: ({ actorUser, page }) => {
      dispatch(
        apiReduxApps.FETCH_ACTIVITY_LOG_DAY_COUNTS_PAGE.operations.start({
          data: {
            actorUser,
            page,
          },
        })
      );
    },
  };
};

const ActivityDashboardBarGraph = connect(
  mapStateToProps,
  mapDispatchToProps
)(ActivityDashboardBarGraphUnconnected);
export default ActivityDashboardBarGraph;
