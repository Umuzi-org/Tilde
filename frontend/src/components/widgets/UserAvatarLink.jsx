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

function getAvatarTextInitials(email) {
  // For Umuzi emails - take the first letters of the name and surname
  if (email.endsWith("umuzi.org")) {
    const [firstname, lastname] = email.split(".");
    return (firstname[0] + lastname[0]).toUpperCase();
  }
  // Other emails - take first two consecutive letters or null if no letters
  const customPartOfAnEmail = email.substr(0, email.indexOf("@"));
  const firstTwoLetters = customPartOfAnEmail.match(/[A-Za-z]{2}/);
  return firstTwoLetters ? firstTwoLetters.join("").toUpperCase() : null;
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
