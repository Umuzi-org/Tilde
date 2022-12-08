import React from "react";
import Paper from "@material-ui/core/Paper";
import Grid from "@material-ui/core/Grid";
import Loading from "../../widgets/Loading";
import { makeStyles } from "@material-ui/core/styles";
import UserBurnDownChart from "./UserBurndownStats";
import ActivityLog from "./ActivityLog";
import Button from "../../widgets/Button";
import ActivityDashboardBarGraph from "./ActivityDashboardBarGraph";

const useStyles = makeStyles((theme) => ({
  column: {
    height: "100%", // TODO. Fit viewport
    overflowY: "scroll",
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
      <Grid container>
        {currentUserBurndownStats && (
          <Grid item xs={12}>
            <Paper className={classes.paper}>
              <UserBurnDownChart burnDownSnapshots={currentUserBurndownStats} />
            </Paper>
          </Grid>
        )}
        <Grid item xs={12}>
          <ActivityDashboardBarGraph eventTypes={eventTypes} />
        </Grid>
        <Grid item xs={12}>
          <Paper>
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
