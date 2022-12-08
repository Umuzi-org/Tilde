import React, { useEffect } from "react";
import { connect } from "react-redux";
import { useParams } from "react-router-dom";

import Presentation from "./Presentation";
import { eventTypeColors } from "../../../../colors";
import { prepareDataForBarGraph } from "./utils";
import { apiReduxApps } from "../../../../apiAccess/apiApps";

export function ActivityDashboardBarGraphUnconnected({
  eventTypes,
  activityLogDayCounts,
  fetchActivityLogDayCountsPage,
}) {
  const { userId } = useParams() || {};
  eventTypes = eventTypes || {};
  activityLogDayCounts = activityLogDayCounts || {};

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
    activityLogDayCounts: state.apiEntities.activityLogDayCounts,
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
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
