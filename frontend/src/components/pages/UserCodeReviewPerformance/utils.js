export function formatTimeString(timestamp) {
  const date = new Date(Date.parse(timestamp));
  return new Intl.DateTimeFormat().format(date);
}
