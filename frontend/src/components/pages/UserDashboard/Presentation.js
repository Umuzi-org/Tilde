import React from "react";
import { Grid, Paper } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";
// import TeamsTable from "../UserDetails/TeamsTable";
import TeamsTable from "../../regions/UserDetails/TeamsTable";
import UserDetailedStats from "./UserDetailedStats";

const useStyles = makeStyles((theme) => ({
  paper: {
    padding: theme.spacing(1),
    margin: theme.spacing(1),
    textAlign: "center",
    color: theme.palette.text.secondary,
  },
}));

export default ({ user, detailedStats, showTeamsTable, authUser }) => {
  const classes = useStyles();
  const teams = user ? user.teamMemberships : {};
  if (user)
    return (
      <React.Fragment>
        <Grid container spacing={1}>
          <Grid item xs={12}>
            <Paper className={classes.paper}>
              <UserDetailedStats detailedStats={detailedStats} />
            </Paper>
          </Grid>
          {showTeamsTable && (
            <Grid item xs={12}>
              <Paper className={classes.paper}>
                <TeamsTable teams={teams} authUser={authUser} />
              </Paper>
            </Grid>
          )}
        </Grid>
      </React.Fragment>
    );
  return <React.Fragment />;
};
