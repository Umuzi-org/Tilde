import TimeAgo from "javascript-time-ago";
import en from "javascript-time-ago/locale/en";
TimeAgo.addDefaultLocale(en);

export function getAgeString(dateString) {
  if (!dateString) return "";
  const date = new Date(dateString);
  const timeAgo = new TimeAgo("en-US");
  /*Age calculated and formatted according to Javascript TimeAgo library.
      Docs link: https://www.npmjs.com/package/javascript-time-ago */
  return timeAgo.format(date);
}

export function repoUrlCleaner(repoUrl) {
  return `${repoUrl
    .slice(0, repoUrl.lastIndexOf(".git"))
    .replace(/git@github.com:/i, "https://github.com/")}/pulls`;
}

export function filterUsers(allUsers) {
  const stringIds = allUsers.filter((user) => typeof user.userId === "string");
  const numberIds = allUsers.filter((user) => typeof user.userId !== "string");

  const reviewers = numberIds.map((obj) => {
    stringIds.map((o) => {
      if (o.email === obj.email) {
        return (obj = o);
      }
    });
    return obj;
  });

  const reviewedUsers = stringIds.filter(
    (firstArrayItem) =>
      !numberIds.some(
        (secondArrayItem) => firstArrayItem.email === secondArrayItem.email
      )
  );

  Array.prototype.push.apply(reviewers, reviewedUsers);
  return reviewers;
}
