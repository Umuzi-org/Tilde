import React, { useEffect } from "react";
import Presentation from "./Presentation";

import { useParams } from "react-router-dom";
import { connect } from "react-redux";

import { eventTypeColors } from "../../../../colors";

export function ActivityDashboardBarGraphUnconnected({
  eventTypes,
  activityLogDayCounts,
}) {
  const x = () => {
    const userActivityLogs = [];

    activityLogDayCounts.forEach((act) => {
      eventTypes.forEach((ev) => {
        if (ev.id === act.eventType) {
          if (
            !userActivityLogs.some(
              (userActivityLog) => userActivityLog.date === act.date
            )
          ) {
            const obj = {};
            obj.date = act.date;
            userActivityLogs.push(Object.assign(obj, { [ev.name]: act.total }));
          } else {
            const dateIndex = userActivityLogs.findIndex(
              (userActivityLog) => userActivityLog.date === act.date
            );
            Object.assign(userActivityLogs[dateIndex], {
              [ev.name]: act.total,
            });
          }
        }
      });
    });
    return userActivityLogs;
  };

  const eventTypeNames = [];

  for (const eventName in eventTypes) {
    eventTypeNames.push(eventTypes[eventName].name);
  }

  const colors = [...Object.values(eventTypeColors)];
  const sortedEventTypeNames = eventTypeNames.sort();
  const evenTypeColorKeys = [...Object.keys(eventTypeColors)].sort();

  for (let i = 0; i < eventTypes.length; i++) {
    if (sortedEventTypeNames[i] === evenTypeColorKeys[i]) {
      eventTypes[i].color = colors[i];
    }
  }

  const props = {
    userActivityLogs,
    eventTypes,
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
