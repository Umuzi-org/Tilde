import React from "react";
import UserActions from "../regions/UserActions/Presentation";
import apis from "../../apiAccess/apis";

import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => ({}));

export default ({ args }) => {
  const classes = useStyles();
  console.log("hello", apis.activityLogDayCountsPage());
  console.log("hello", UserActions({ args }));
  return <UserActions {...args} />;
};
