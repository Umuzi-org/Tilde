export function addEventColorsToLogEntries({
  eventTypes,
  eventTypeColors,
  activityLogEntries,
}) {
  const eventTypesWithEventNames = [];
  // eventTypes = Object.keys(eventTypes).map((key) => eventTypes[key]);
  const eventTypesArray = Object.values(eventTypes);

  eventTypesArray.forEach((eventType) => {
    eventTypesWithEventNames.push({
      id: eventType.id,
      eventName: eventType.name,
      eventColor: eventTypeColors[eventType.name],
    });
  });

  activityLogEntries = Object.keys(activityLogEntries).map(
    (key) => activityLogEntries[key]
  );

  const newData = activityLogEntries.map((item, index) => {
    const data = eventTypesWithEventNames.find(
      (elem) => elem.id === item.eventType
    );
    return {
      ...item,
      eventName: data ? data.eventName : "",
      eventColor: data ? data.eventColor : "",
    };
  });
  return newData;
}

export function fillInSnapshotDateGaps({ burnDownSnapshots }) {
  const datesArray = burnDownSnapshots.map((burnDownSnapshot) => {
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
      self.findIndex(
        (t) =>
          t.timestamp === burnDownSnapshot.timestamp &&
          t.cardsInCompleteColumnTotalCount ===
            burnDownSnapshot.cardsInCompleteColumnTotalCount
      )
  );
  return result;
}
