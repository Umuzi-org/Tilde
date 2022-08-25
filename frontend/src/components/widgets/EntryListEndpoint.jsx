import React from "react";
import UserActions from "../regions/UserActions/Presentation";
import apis from "../../apiAccess/apis";

import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => ({}));

export default ({ args }) => {
  const classes = useStyles();
  console.log(
    "hello",
    apis
      .activityLogDayCountsPage({
        eventTypeName: "git_real | pull request review",
        actorUser: 18,
        effectedUser: 2,
        page: 1,
      })
      .then((data) => console.log(data))
  );
  console.log("hello", UserActions({ args }));
  return <UserActions {...args} />;
};
