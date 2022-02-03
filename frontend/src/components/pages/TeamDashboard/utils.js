export const getMinAndMaxDate = ({ activityLogDayCounts }) => {
  const datesArray = [];
  for (let i in activityLogDayCounts) {
    activityLogDayCounts[i].forEach((activityLogDayCount) => {
      datesArray.push(activityLogDayCount.date);
    });
  }

  const sortedActivityLogDayCounts = datesArray.sort(
    (a, b) => new Date(a) - new Date(b)
  );

  const minimumDate = sortedActivityLogDayCounts[0];
  const maximumDate =
    sortedActivityLogDayCounts[sortedActivityLogDayCounts.length - 1];

  return {
    minimumDate,
    maximumDate,
  };
};
