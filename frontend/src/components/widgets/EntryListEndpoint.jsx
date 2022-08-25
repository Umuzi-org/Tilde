import React from "react";
import UserActions from "../regions/UserActions/Presentation";

import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => ({}));

export default ({ args }) => {
  const classes = useStyles();
  console.log("hello");
  console.log("hello", UserActions({ args }));
  return <UserActions {...args} />;
};
