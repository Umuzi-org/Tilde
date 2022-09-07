import React from "react";
import { Link } from "react-router-dom";
import Avatar from "@material-ui/core/Avatar";
import Typography from "@material-ui/core/Typography";
import { makeStyles } from "@material-ui/styles";
import { getUrl as getUserBoardUrl } from "./LinkToUserBoard";

const useStyles = makeStyles({
  avatarLink: {
    textDecoration: "none",
    marginRight: 8,
  },
  container: {
    display: "flex",
    alignItems: "center",
  },
});

export function getAvatarInitials(email) {
  const alphanumerals = /[a-zA-Z0-9]/;
  const emailUsername = email.substr(0, email.indexOf("@"));
  if (email.endsWith("umuzi.org")) {
    const [firstname, lastname] = emailUsername.split(".");
    return (firstname[0] + lastname[0]).toUpperCase();
  }
  let firstTwoLetters = "";
  for (let i = 0; i < emailUsername.length; i++) {
    if (alphanumerals.test(emailUsername[i]))
      firstTwoLetters += emailUsername[i];
    if (firstTwoLetters.length === 2) return firstTwoLetters.toUpperCase();
  }
}

function UserAvatarLink({ email, userId }) {
  const classes = useStyles();
  return (
    <div className={classes.container}>
      <Link to={getUserBoardUrl({ userId })} className={classes.avatarLink}>
        <Avatar>{getAvatarInitials(email)}</Avatar>
      </Link>
      <Typography>{email}</Typography>
    </div>
  );
}

export default UserAvatarLink;
