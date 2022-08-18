import React from "react";
import { Link } from "react-router-dom";
import Avatar from "@material-ui/core/Avatar";
import Typography from "@material-ui/core/Typography";
import { makeStyles } from "@material-ui/styles";
import { getUrl as getUserBoardUrl } from "./LinkToUserBoard";

const useStyles = makeStyles({
  avatarLink: {
    textDecoration: "none",
  },
  container: {
    display: "flex",
    alignItems: "center",
    gap: 8,
  },
});

export function getAvatarTextInitials(email) {
  if (email.endsWith("umuzi.org")) {
    const [firstname, lastname] = email.split(".");
    return (firstname[0] + lastname[0]).toUpperCase();
  }
  const firstTwoLetters = email.match(/^[A-Za-z]{2}/);
  return firstTwoLetters && firstTwoLetters.join("").toUpperCase();
}

function UserAvatarLink({ email, userId }) {
  const classes = useStyles();
  return (
    <div className={classes.container}>
      <Link to={getUserBoardUrl({ userId })} className={classes.avatarLink}>
        <Avatar>{getAvatarTextInitials(email)}</Avatar>
      </Link>
      <Typography>{email}</Typography>
    </div>
  );
}

export default UserAvatarLink;
