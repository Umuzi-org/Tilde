export function randomDateBetweenCurrentDayAnd21DaysAgo() {
  let todayDate = new Date();
  let _21DaysAgoDate = new Date(new Date().setDate(new Date().getDate() - 21));

  todayDate = todayDate.getTime();
  _21DaysAgoDate = _21DaysAgoDate.getTime();

  const randomDate = new Date(
    todayDate + Math.random() * (_21DaysAgoDate - todayDate)
  );

  const formattedRandomDate = `${randomDate.getFullYear()}-${
    randomDate.getMonth() + 1
  }-${randomDate.getDate()}`;

  return formattedRandomDate;
}
