import React from "react";
import { Grid, Paper, Typography } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import ReviewTrustTable from "../UserDetails/ReviewTrustTable/Presentation";
import TeamsTable from "../UserDetails/TeamsTable/Presentation";

const useStyles = makeStyles((theme) => ({
  paper: {
    padding: theme.spacing(1),
    margin: theme.spacing(1),
    textAlign: 'center',
    color: theme.palette.text.secondary,
  },
}));

export default () => {
  const classes = useStyles();
  
  return (
    <React.Fragment>
      <Grid container spacing={1}>
        <Grid item xs={12}>
          <Paper className={classes.paper}>
            <Typography>TEAMS</Typography>
            <TeamsTable />
          </Paper>
        </Grid>
        <Grid item xs={12}>
          <Paper className={classes.paper}>
            <Typography>REVIEW TRUSTS</Typography>
            <ReviewTrustTable />
          </Paper>
        </Grid>
      </Grid>
    </React.Fragment>
  )
};