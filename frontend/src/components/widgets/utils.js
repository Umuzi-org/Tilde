import TimeAgo from "javascript-time-ago";
import en from "javascript-time-ago/locale/en";
TimeAgo.addDefaultLocale(en);

export const getAgeString = (dateString) => {
  if (!dateString) return "";
  const date = new Date(dateString);
  const timeAgo = new TimeAgo("en-US");
  /*Age calculated and formatted according to Javascript TimeAgo library.
      Docs link: https://www.npmjs.com/package/javascript-time-ago */
  return timeAgo.format(date);
};
