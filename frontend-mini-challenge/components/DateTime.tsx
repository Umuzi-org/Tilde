import { parseISO, format } from "date-fns";

export function DateTime({ timestamp }: { timestamp: string }) {
  const date = parseISO(timestamp);
  return (
    <time dateTime={timestamp}>{format(date, "HH:MM - d LLLL yyyy")}</time>
  );
}
