export function prepareDataForBarGraph({ eventTypes, activityLogDayCounts }) {
  const eventNames = {};
  Object.values(eventTypes).forEach(
    (eventType) => (eventNames[eventType.id] = eventType["name"])
  );

  const result = {};
  Object.values(activityLogDayCounts).forEach((dayCount) => {
    const { date, eventType } = dayCount;
    const eventName = eventNames[eventType];
    result[date] = result[date] || { date };
    result[date][eventName] = dayCount.total;
  });

  return Object.values(result);
}

export function replaceUnderscoresWithSpace(str) {
  return str.toLowerCase().replaceAll("_", " ");
}
