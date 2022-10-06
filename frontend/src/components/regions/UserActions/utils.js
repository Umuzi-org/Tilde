export function matchEventTypesWithColors({ eventTypes, eventTypeColors }) {
  const arr = [];
  eventTypes = Object.keys(eventTypes).map((key) => eventTypes[key]);

  eventTypes.forEach((eventType) => {
    arr.push({
      id: eventType.id,
      eventName: eventType.name,
      eventColor: eventTypeColors[eventType.name],
    });
  });
  return arr;
}

export function addEventColorsToLogEntries({
  eventTypesWithColors,
  activityLogEntries,
}) {
  activityLogEntries = Object.keys(activityLogEntries).map(
    (key) => activityLogEntries[key]
  );

  const newData = activityLogEntries.map((item, index) => {
    const data = eventTypesWithColors.find(
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
