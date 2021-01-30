import React from "react";

import { Typography, Toolbar } from "@material-ui/core";

import LinkToUserBoard from "../../widgets/LinkToUserBoard";
import LinkToUserActions from "../../widgets/LinkToUserActions";

import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => ({
  grow: { flexGrow: 1 },
  toolbar: {
    margin: theme.spacing(0.5),
    border: "1px solid grey",
  },
  button: { marginRight: theme.spacing(1) },
}));

export default ({ user, userBoardSelected, UserActionsSelected }) => {
  const classes = useStyles();
  const userId = user && user.id;
  return (
    <React.Fragment>
      <Toolbar variant="dense" className={classes.toolbar}>
        <div className={classes.button}>
          <LinkToUserBoard userId={userId} selected={userBoardSelected} />
        </div>
        <div className={classes.button}>
          <LinkToUserActions userId={userId} selected={UserActionsSelected} />
        </div>
        <div className={classes.grow} />
        {user && <Typography>Viewing: {user.email}</Typography>}
      </Toolbar>
    </React.Fragment>
  );
};
