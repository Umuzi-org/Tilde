import React from "react";
import { Grid, Paper, Typography } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import TeamsTable from "../UserDetails/TeamsTable";

const useStyles = makeStyles((theme) => ({
  paper: {
    padding: theme.spacing(1),
    margin: theme.spacing(1),
    textAlign: 'center',
    color: theme.palette.text.secondary,
  },
}));

export default ({ 
  user, 
  userId 
}) => {
  const classes = useStyles();
  const teams =  user ? user.teamMemberships : {};
  if(userId)
    return (
      <React.Fragment>
        <Grid container spacing={1}>
          <Grid item xs={12}>
            <Paper className={classes.paper}>
              <Typography>You are a member of these teams:</Typography>
              <TeamsTable teams={teams} />
            </Paper>
          </Grid>
        </Grid>
      </React.Fragment>
    );
  return <React.Fragment />;  
};