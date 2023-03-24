import { parseISO, format } from "date-fns";

export function DateTime({ timestamp }) {
  const date = parseISO(timestamp);
  return <time dateTime={timestamp}>{format(date, "LLLL d, yyyy")}</time>;
}
