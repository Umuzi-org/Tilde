import React from "react";
import Avatar from "@material-ui/core/Avatar";
import Typography from "@material-ui/core/Typography";

function UserAvatarLink({ email, userId }) {
  return (
    <div>
      <Avatar>{email.slice(0, 2).toUpperCase()}</Avatar>
      <Typography>{email}</Typography>
    </div>
  );
}

export default UserAvatarLink;
