export const getActivityLogCountsByDayForUsers = ({ userIds, activityLogDayCounts, eventTypes, }) => {
  let result = {};
  const sortedActivityLogDayCounts = activityLogDayCounts.sort((a, b) => new Date(a) - new Date(b));
  const minDate = sortedActivityLogDayCounts[0].date;
  const maxDate = sortedActivityLogDayCounts[sortedActivityLogDayCounts.length - 1].date;

  userIds.forEach(
    (userId) =>
      (result[userId] = getActivityLogCountsByDayForSingleUser({
        userId,
        activityLogDayCounts,
        eventTypes,
      }))
  );
  return result;
};

export const getActivityLogCountsByDayForSingleUser = ({
  // TODO: take in start and end dates and make sure all the dates have a value
  userId,
  activityLogDayCounts,
  eventTypes,
}) => {
  const zeroes = {};
  eventTypes.forEach((element) => {
    zeroes[element] = 0;
  });
  const userLogs = activityLogDayCounts.filter(
    (element) =>
      element.id.match(`actor_user=${userId}$`) ||
      element.id.match(`actor_user=${userId}&`) ||
      element.id.match(`effected_user=${userId}$`) ||
      element.id.match(`effected_user=${userId}&`)
  );

  const resultByDate = {};

  eventTypes.forEach((eventType) => {
    const userLogsFilteredByType = userLogs.filter(
      (element) =>
        element.id.match(`event_type__name=${eventType}&`) ||
        element.id.match(`event_type__name=${eventType}$`)
    );

    userLogsFilteredByType.forEach((entry) => {
      if (resultByDate[entry.date] === undefined) {
        resultByDate[entry.date] = {
          date: entry.date,
          ...zeroes,
          [eventType]: entry.total,
        };
      } else {
        resultByDate[entry.date][eventType] = entry.total;
      }
    });
  });

  return Object.values(resultByDate);
};
