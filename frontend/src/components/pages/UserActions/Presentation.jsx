import React from "react";
import Paper from "@material-ui/core/Paper";
import Grid from "@material-ui/core/Grid";
import Loading from "../../widgets/Loading";
import { makeStyles } from "@material-ui/core/styles";
import UserBurnDownChart from "./UserBurndownStats";
import ActivityLog from "./ActivityLog";
import Button from "../../widgets/Button";
import ActivityDashboardBarGraph from "./ActivityDashboardBarGraph";
import { Typography } from "@material-ui/core";

const useStyles = makeStyles((theme) => ({
  column: {
    height: "100%", // TODO. Fit viewport
    overflowY: "scroll",
  },
  paper: {
    padding: theme.spacing(1),
  },
  sectionHeading: {
    fontSize: 40,
    textAlign: "center",
  },
}));

export default function Presentation({
  orderedDates,
  handleScroll,
  anyLoading,
  currentUserBurndownStats,
  activityLogEntries,
  fetchNextPages,
  eventTypes,
}) {
  const classes = useStyles();
  return (
    <div className={classes.column} onScroll={handleScroll}>
      <Grid container spacing={2}>
        {currentUserBurndownStats && (
          <Grid item xs={12}>
            <Paper className={classes.paper}>
              <Typography variant="h2" className={classes.sectionHeading}>
                Burn Chart
              </Typography>
              <UserBurnDownChart burnDownSnapshots={currentUserBurndownStats} />
            </Paper>
          </Grid>
        )}
        <Grid item xs={12}>
          <ActivityDashboardBarGraph eventTypes={eventTypes} />
        </Grid>
        <Grid item xs={12}>
          <Paper className={classes.paper}>
            <Typography variant="h2" className={classes.sectionHeading}>
              Event Log
            </Typography>
            <ActivityLog
              eventList={activityLogEntries}
              orderedDates={orderedDates}
            />
            <Button onClick={fetchNextPages}>Load More</Button>

            {anyLoading && <Loading />}
          </Paper>
        </Grid>
      </Grid>
    </div>
  );
}
