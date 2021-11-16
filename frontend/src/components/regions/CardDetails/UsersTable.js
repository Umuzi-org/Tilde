import React from "react";
import { Typography } from "@mui/material";

export default ({ userNames, userIds }) => {
  return <Typography>{userNames.join(", ")}</Typography>;
};
