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

// TODO: helper for getting the two letters for avatar
// - if the user has an umuzi email:
//      - use get the first letter in the firstname and lastname of the email
// - else:
//      - use first two characters of the email

function UserAvatarLink({ email, userId }) {
  const classes = useStyles();
  return (
    <div className={classes.container}>
      <Link to={getUserBoardUrl({ userId })} className={classes.avatarLink}>
        <Avatar>{email.slice(0, 2).toUpperCase()}</Avatar>
      </Link>
      <Typography>{email}</Typography>
    </div>
  );
}

export default UserAvatarLink;
