export function randomDateBetweenCurrentDayAnd21DaysAgo() {
  let todayDate = new Date();
  let daysAgoDate = new Date(new Date().setDate(new Date().getDate() - 21));

  todayDate = todayDate.getTime();
  daysAgoDate = daysAgoDate.getTime();

  const randomDate = new Date(
    todayDate + Math.random() * (daysAgoDate - todayDate)
  );

  const formattedRandomDate = `${randomDate.getFullYear()}-${
    randomDate.getMonth() + 1
  }-${randomDate.getDate()}`;

  return formattedRandomDate;
}
