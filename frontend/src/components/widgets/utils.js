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

export const canSetDueTime = (card, authUser) => {

  if(!card.dueTime && authUser.email === card.assigneeNames[0]) {
    return true;
  } 

  if(!card.dueTime && authUser.email === card.assigneeNames[0] && Object.keys(authUser.permissions.teams).map((key) => authUser.permissions.teams[key].permissions[0]).length !== 0) {
    return true;
  }

  if(!card.dueTime && authUser.email !== card.assigneeNames[0] && Object.keys(authUser.permissions.teams).map((key) => authUser.permissions.teams[key].permissions[0]).includes("MANAGE_CARDS")) {
    return true;
  }

  return false;
}