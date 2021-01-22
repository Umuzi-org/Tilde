import React from "react";

import { Paper } from "@material-ui/core";

import LinkToUserBoard from "../../widgets/LinkToUserBoard";
import LinkToUserStats from "../../widgets/LinkToUserStats";

import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => ({}));

export default ({ userId, userBoardSelected, userStatsSelected }) => {
  const classes = useStyles();
  return (
    <Paper>
      <LinkToUserBoard
        className={classes.button}
        userId={userId}
        selected={userBoardSelected}
      />
      <LinkToUserStats
        className={classes.button}
        userId={userId}
        selected={userStatsSelected}
      />
    </Paper>
  );
};
