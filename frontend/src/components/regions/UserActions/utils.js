export function updateBurnDownSnapshots({
  burnDownSnapshots,
  filterStartDate,
}) {
  const datesArray = [];
  //console.log(datesArray);

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
  //console.log(datesArray);

  for (let uniqueDate of allDatesArr) {
    if (
      !burnDownSnapshots.some(
        (burnDownSnapshot) => burnDownSnapshot.date === uniqueDate
      )
    ) {
      burnDownSnapshots.push({
        cardsInCompleteColumnTotalCount:
          burnDownSnapshots.cardsInCompleteColumnTotalCount,
        cardsTotalCount: burnDownSnapshots.cardsTotalCount,
        id: burnDownSnapshots.id,
        projectCardsInCompleteColumnTotalCount:
          burnDownSnapshots.projectCardsInCompleteColumnTotalCount,
        projectCardsTotalCount: burnDownSnapshots.projectCardsTotalCount,
        timestamp: uniqueDate,
        user: burnDownSnapshots.user,
      });
    }
  }
  //   return  burnDownSnapshots;
  // }
  //const updatedBurnDownSnapshots = {};
    burnDownSnapshots = burnDownSnapshots.reduce((unique, o) => {
    if (!unique.some((obj) => obj.timestamp === o.timestamp)) {
      unique.push(o);
    }
    return unique;
  }, []);
  console.log(burnDownSnapshots);
  return burnDownSnapshots;
  
}
