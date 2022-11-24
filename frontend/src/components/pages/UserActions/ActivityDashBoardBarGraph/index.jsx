import React from "react";
import Presentation from "./Presentation";

import { connect } from "react-redux";

import { eventTypeColors } from "../../../../colors";
import { prepareDataForBarGraph } from "./utils";

export function ActivityDashboardBarGraphUnconnected({
  eventTypes,
  activityLogDayCounts,
}) {
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

const mapStateToProps = (state) => {};

const mapDispatchToProps = (dispatch) => {};

const ActivityDashboardBarGraph = connect(
  mapStateToProps,
  mapDispatchToProps
)(ActivityDashboardBarGraphUnconnected);
export default ActivityDashboardBarGraph;
