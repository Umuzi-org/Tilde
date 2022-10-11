export function addEventColorsToLogEntries({
  eventTypes, 
  eventTypeColors,
  activityLogEntries,
}) {

  const eventTypesWithEventNames = [];
  eventTypes = Object.keys(eventTypes).map((key) => eventTypes[key]);

  eventTypes.forEach((eventType) => {
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
