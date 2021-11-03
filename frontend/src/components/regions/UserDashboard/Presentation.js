import React from "react";
import { Grid, Paper } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";
import TeamsTable from "../UserDetails/TeamsTable";
import UserDetailedStats from "./UserDetailedStats";

// TODO: should we include the user teams here?

const useStyles = makeStyles((theme) => ({
  paper: {
    padding: theme.spacing(1),
    margin: theme.spacing(1),
    textAlign: "center",
    color: theme.palette.text.secondary,
  },
}));

export default ({ user, detailedStats }) => {
  const classes = useStyles();
  // const teams = user ? user.teamMemberships : {};
  if (user)
    return (
      <React.Fragment>
        <Grid container spacing={1}>
          <Grid item xs={12}>
            <Paper className={classes.paper}>
              <UserDetailedStats detailedStats={detailedStats} />
            </Paper>
          </Grid>
          {/* <Grid item xs={12}>
            <Paper className={classes.paper}>
              <TeamsTable teams={teams} />
            </Paper>
          </Grid> */}
        </Grid>
      </React.Fragment>
    );
  return <React.Fragment />;
};
