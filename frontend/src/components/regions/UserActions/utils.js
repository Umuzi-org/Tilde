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
  console.log(datesArray);

  // for (let i = 0; i < allDatesArr.length; i++) {
  //   if (
  //     !(burnDownSnapshots.timestamp === uniqueDatesArr[i])
  //     )
  //   {
  //     burnDownSnapshots.push({
  //       cardsInCompleteColumnTotalCount:burnDownSnapshots[i].cardsInCompleteColumnTotalCount,
  //       cardsTotalCount: burnDownSnapshots[i].cardsTotalCount,
  //       id: burnDownSnapshots[i].id,
  //       projectCardsInCompleteColumnTotalCount: burnDownSnapshots[i].projectCardsInCompleteColumnTotalCount,
  //       projectCardsTotalCount: burnDownSnapshots[i].projectCardsTotalCount,
  //       timestamp: uniqueDatesArr[i],
  //       user: burnDownSnapshots[i].user,
  //     });
  //   }
  // }
  // for (let i in burnDownSnapshots) {
  //     for (let uniqueDate of allDatesArr) {
  //       if (
  //         !burnDownSnapshots[i].some(
  //           (burnDownSnapshot) => burnDownSnapshot.timestamp === uniqueDate
  //         )
  //       ) {
  //         burnDownSnapshots[i].push({
  //           cardsInCompleteColumnTotalCount:
  //             burnDownSnapshots[i].cardsInCompleteColumnTotalCount,
  //           cardsTotalCount: burnDownSnapshots[i].cardsTotalCount,
  //           id: burnDownSnapshots.id,
  //           projectCardsInCompleteColumnTotalCount:
  //             burnDownSnapshots[i].projectCardsInCompleteColumnTotalCount,
  //           projectCardsTotalCount: burnDownSnapshots[i].projectCardsTotalCount,
  //           timestamp: uniqueDate,
  //           user: burnDownSnapshots[i].user,
  //         });
  //       }
  //     }
  //   }
  // const res = [];
  // while (datesArray.length > 0) {
  //   const chunk = datesArray.splice(0, 2);
  //   res.push(chunk);
  // }
  //console.log(res);
  var getDaysArray = function (start, end) {
    for (
      var arr = [], dt = new Date(start);
      dt <= new Date(end);
      dt.setDate(dt.getDate() + 1)
    ) {
      arr.push(new Date(dt).toISOString().split("T")[0]);
    }
    return arr;
  };
  let z = [];
  for (let i = 0; i < datesArray.length; i++) {
    z.push(getDaysArray(datesArray[i], datesArray[i + 1]));
  }

  console.log(z);
  //console.log(getDaysArray(res[0][0], res[0][1]));

  //console.log(res);
  //   return  burnDownSnapshots;
  // }
  //const updatedBurnDownSnapshots = {};
  for (let uniqueDate of allDatesArr) {
    if (
      !burnDownSnapshots.some(
        (burnDownSnapshot) => burnDownSnapshot.date === uniqueDate
      )
    ) {
      burnDownSnapshots.push({
        cardsInCompleteColumnTotalCount: 150,
        cardsTotalCount: 160,
        id: burnDownSnapshots.id,
        projectCardsInCompleteColumnTotalCount: 150,
        projectCardsTotalCount: 160,
        timestamp: uniqueDate,
        user: 425,
      });
    }
  }

  burnDownSnapshots = burnDownSnapshots.reduce((unique, o) => {
    if (!unique.some((obj) => obj.timestamp === o.timestamp)) {
      unique.push(o);
    }
    return unique;
  }, []);
  burnDownSnapshots = burnDownSnapshots.sort(function (a, b) {
    var c = new Date(a.timestamp);
    var d = new Date(b.timestamp);
    return c - d;
  });
  //console.log(burnDownSnapshots);
  return burnDownSnapshots;
}
