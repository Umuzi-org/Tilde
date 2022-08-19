import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Paper from "@material-ui/core/Paper";
import Grid from "@material-ui/core/Grid";
import Button from "@material-ui/core/Button";
import Typography from "@material-ui/core/Typography"

import ProfilePicture from "./ProfilePicture"
import UserProfileDetails from "./UserProfileDetails";
import NickName from "./NickName"

const useStyles = makeStyles((theme) => ({
  root: {
    maxHeight: "90vh",
    maxWidth: "90vw",
    display: "flex",
     flexFlow: "row nowrap",
    alignItems: "center",
    justifyContent: "center",
  },
  paper: {
    padding: theme.spacing(0),
    textAlign: "center",
    color: theme.palette.text.secondary,
    height: "40vh",
    display: "flex",
    flexFlow: "row nowrap",
    justifyContent: "center",
    alignItems: "center",
    textTransform: "none",
  },
}));

export default function UserProfile() {
  const classes = useStyles();

  return (
    <div className={classes.root}>
      
      <Grid container spacing={0} direction="row" justifyContent="center" alignItems="center">
        <Grid item xs={12} md={6} lg={6}>
          <Paper className={classes.paper}>
            <ProfilePicture />
          </Paper>
        </Grid>
        <Grid item xs={12} md={6} lg={6}>
          <Paper className={classes.paper}>
            <UserProfileDetails />
          </Paper>
        </Grid>
      </Grid>
      
    </div>
  );
}
