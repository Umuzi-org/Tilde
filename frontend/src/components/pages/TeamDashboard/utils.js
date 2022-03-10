export const updateActivityLogDayCounts = ({ activityLogDayCounts }) => {
  const datesArray = [];
  for (let i in activityLogDayCounts) {
    activityLogDayCounts[i].forEach((activityLogDayCount) => {
      datesArray.push(activityLogDayCount.date);
    });
  }

  const uniqueDatesArr = Array.from(new Set(datesArray)).sort(
    (a, b) => new Date(a) - new Date(b)
  );

  const firstDate = new Date(new Date(uniqueDatesArr[0]).getTime());
  const lastDate = new Date(uniqueDatesArr[uniqueDatesArr.length - 1]);
  const allDatesArr = [];

  while (firstDate <= lastDate) {
    allDatesArr.push(new Date(firstDate).toISOString().split("T")[0]);
    firstDate.setDate(firstDate.getDate() + 1);
  }

  for (let i in activityLogDayCounts) {
    for (let uniqueDate of allDatesArr) {
      if (
        !activityLogDayCounts[i].some(
          (activityLogDayCount) => activityLogDayCount.date === uniqueDate
        )
      ) {
        activityLogDayCounts[i].push({
          date: uniqueDate,
          COMPETENCE_REVIEW_DONE: 0,
          PR_REVIEWED: 0,
        });
      }
    }
  }

  const updatedActivityLogDayCounts = {};

  Object.entries(activityLogDayCounts).forEach((activityLogDayCount) => {
    updatedActivityLogDayCounts[activityLogDayCount[0]] =
      activityLogDayCount[1].sort(
        (a, b) => new Date(a.date) - new Date(b.date)
      );
  });

  return updatedActivityLogDayCounts;
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
