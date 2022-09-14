export function updateburnDownSnapshots({ burnDownSnapshots, filterStartDate }) {
    const datesArray = [];
    for (let i in burnDownSnapshots) {
      burnDownSnapshots[i].forEach((activityLogDayCount) => {
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
  
    for (let i in burnDownSnapshots) {
      for (let uniqueDate of allDatesArr) {
        if (
          !burnDownSnapshots[i].some(
            (activityLogDayCount) => activityLogDayCount.date === uniqueDate
          )
        ) {
          burnDownSnapshots[i].push({
            timestamp: uniqueDate,
            cardsInCompleteColumnTotalCount: 0,
          });
        }
      }
    }
  
    const updatedburnDownSnapshots = {};
    Object.entries(burnDownSnapshots).forEach((activityLogDayCount) => {
      updatedburnDownSnapshots[
        activityLogDayCount[0]
      ] = activityLogDayCount[1].sort(
        (a, b) => new Date(a.date) - new Date(b.date)
      ).filter(
        (activity) => new Date(activity.date) >= filterStartDate
      );
    });
    return updatedburnDownSnapshots;
  }