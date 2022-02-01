export const getMinAndMaxDate = ({ activityLogDayCounts }) => {
  const sortedActivityLogDayCounts = activityLogDayCounts.sort(
    (a, b) => new Date(a) - new Date(b)
  );
  const minimumDate = sortedActivityLogDayCounts[0].date;
  const maximumDate =
    sortedActivityLogDayCounts[sortedActivityLogDayCounts.length - 1].date;

  return {
    minimumDate,
    maximumDate,
  };
};
