import React from "react";

import Grid from "@material-ui/core/Grid";
import Paper from "@material-ui/core/Paper";
import { makeStyles } from "@material-ui/core/styles";
import Typography from "@material-ui/core/Typography";

import NickName from "./NickName";
import ProfilePicture from "./ProfilePicture";
import UserProfileDetails from "./UserProfileDetails";

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
      <Grid
        style={{ width: "70%", height: "70%", position: "relative", top: 90 }}
        container="true"
        spacing={0}
        direction="row"
        justifyContent="center"
        alignItems="center"
      >
        <Grid item xs={12} md={6} lg={6}>
          <Paper className={classes.paper} elevation={6}>
            <ProfilePicture />
          </Paper>
        </Grid>
        <Grid item xs={12} md={6} lg={6}>
          <Paper
            className={classes.paper}
            elevation={6}
            style={{ position: "relative" }}
          >
            <div style={{ position: "absolute", top: 30 }}>
              <Typography variant="h3">
                First Name
                <Typography variant="h5">
                  <NickName />
                </Typography>
              </Typography>
            </div>
            <UserProfileDetails style={{ position: "relative", top: 60 }} />
          </Paper>
        </Grid>
      </Grid>
    </div>
  );
}
