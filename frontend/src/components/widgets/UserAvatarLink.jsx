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
  const customPartOfAnEmail = email.substr(0, email.indexOf("@"));
  // For Umuzi emails - take the first letters of the firstname and lastname
  if (email.endsWith("umuzi.org")) {
    const [firstname, lastname] = customPartOfAnEmail.split(".");
    return (firstname[0] + lastname[0]).toUpperCase();
  }
  // Other emails - take first two letters/digits
  let firstTwoLetters = "";
  const alphanumerals = /[a-zA-Z0-9]/;
  for (let i = 0; i < customPartOfAnEmail.length; i++) {
    if (alphanumerals.test(customPartOfAnEmail[i]))
      firstTwoLetters += customPartOfAnEmail[i];
    if (firstTwoLetters.length === 2) return firstTwoLetters.toUpperCase();
  }
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
