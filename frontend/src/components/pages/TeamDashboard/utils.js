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

export const getMinimumAndMaximumValue = ({ activityLogDayCounts }) => {
  const numbersArr = [];
  for (let i in activityLogDayCounts) {
    activityLogDayCounts[i].forEach((arrValues) => {
      numbersArr.push(arrValues.COMPETENCE_REVIEW_DONE, arrValues.PR_REVIEWED);
    });
  }
  const minValue = Math.min(...numbersArr);
  const maxValue = Math.max(...numbersArr);
  return { minValue, maxValue };
};
