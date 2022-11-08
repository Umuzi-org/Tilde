export function prepareDataForBarGraph({ eventTypes, activityLogDayCounts }) {
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
}
