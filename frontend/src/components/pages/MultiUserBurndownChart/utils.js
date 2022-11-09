export function fillInSnapshotDateGaps({ currentUserBurndownStats }) {
  const datesArray = currentUserBurndownStats.map((burnDownSnapshot) => {
    return burnDownSnapshot.timestamp;
  });
  const firstDate = new Date(new Date(datesArray[0]).getTime());
  const lastDate = new Date(datesArray[datesArray.length - 1]);
  const allDatesArr = [];

  while (firstDate <= lastDate) {
    allDatesArr.push(new Date(firstDate).toISOString().split("T")[0]);
    firstDate.setDate(firstDate.getDate() + 1);
  }
  const getDaysArray = function (start, end) {
    let gapDates = [];
    const theDate = new Date(start);
    while (theDate < new Date(end)) {
      gapDates = [...gapDates, new Date(theDate)];
      theDate.setDate(theDate.getDate() + 1);
    }
    gapDates = [...gapDates, new Date(end)];
    return gapDates;
  };

  const subArrayDates = [];
  for (let i = 0; i < currentUserBurndownStats.length; i++) {
    subArrayDates.push(getDaysArray(datesArray[i], datesArray[i + 1]));
    subArrayDates[i].pop();
  }

  const newcurrentUserBurndownStats = [];
  for (let i = 0; i < subArrayDates.length; ++i) {
    const subArray = subArrayDates[i];
    for (let j = 0; j < subArray.length; ++j) {
      subArray[j] = currentUserBurndownStats[i];
      newcurrentUserBurndownStats.push(subArray[j]);
    }
  }

  const result = allDatesArr.map((indexPosition, i) => {
    return { ...newcurrentUserBurndownStats[i], timestamp: indexPosition };
  });
  result[result.length - 1] = currentUserBurndownStats[currentUserBurndownStats.length - 1];
  return result;
}
