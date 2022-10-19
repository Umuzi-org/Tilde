export function filterByStartDate(numberOfDays) {
  const filterStartDate = new Date();
  filterStartDate.setDate(filterStartDate.getDate() - numberOfDays);

  const newDate = `${filterStartDate.getFullYear()}-${
    filterStartDate.getMonth() + 1
  }-${filterStartDate.getDate()}`;

  return newDate;
}
