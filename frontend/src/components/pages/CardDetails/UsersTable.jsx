import React from "react";
import { Typography } from "@material-ui/core";

export default ({ userNames, userIds }) => {
  return <Typography>{userNames.join(", ")}</Typography>;
};
