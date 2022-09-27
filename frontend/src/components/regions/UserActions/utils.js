export function updateBurnDownSnapshots({ burnDownSnapshots }) {
  const datesArray = [];
  burnDownSnapshots.forEach((burnDownSnapshot) => {
    datesArray.push(burnDownSnapshot.timestamp);
  });

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
  for (let i = 0; i < burnDownSnapshots.length; i++) {
    subArrayDates.push(getDaysArray(datesArray[i], datesArray[i + 1]));
    subArrayDates[i].pop();
  }

  const newBurnDownSnapshots = [];
  for (let i = 0; i < subArrayDates.length; ++i) {
    const subArray = subArrayDates[i];
    for (let j = 0; j < subArray.length; ++j) {
      subArray[j] = burnDownSnapshots[i];
      newBurnDownSnapshots.push(subArray[j]);
    }
  }

  const result = allDatesArr.map((indexPosition, i) => {
    return { ...newBurnDownSnapshots[i], timestamp: indexPosition };
  });
  result[result.length - 1] = burnDownSnapshots[burnDownSnapshots.length - 1];

  return result;
}

export function removeDuplicateDates({ burnDownSnapshots }) {
  const result = burnDownSnapshots.filter(
    (burnDownSnapshot, index, self) =>
      index ===
      self.findIndex((t) => t.timestamp === burnDownSnapshot.timestamp)
  );
  return result;
}
