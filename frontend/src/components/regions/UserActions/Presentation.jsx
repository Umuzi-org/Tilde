import React from "react";
import Paper from "@material-ui/core/Paper";
import Grid from "@material-ui/core/Grid";
import Loading from "../../widgets/Loading";
import { makeStyles } from "@material-ui/core/styles";
import DayLog from "./DayLog";
import ActivityDashboardBarGraph from "../../pages/UserDashboard/ActivityDashboardBarGraph";

const useStyles = makeStyles((theme) => ({
  column: {
    height: "85%", // TODO. Fit viewport
    overflowY: "scroll",
  },
}));

export default function Presentation({
  orderedDates,
  actionLogByDate,
  handleClickOpenProjectDetails,
  handleScroll,
  anyLoading,
}) {
  const classes = useStyles();
  return (
    <div
      className={classes.column}
      onScroll={handleScroll}
      style={{ position: "relative" }}
    >
      <Grid container spacing={2}>
        <Grid item xs={12} md={4} lg={4}>
          <Paper>
            {orderedDates.map((date) => (
              <DayLog
                date={date}
                key={date}
                actions={actionLogByDate[date]}
                handleClickOpenProjectDetails={handleClickOpenProjectDetails}
              />
            ))}

            {anyLoading && <Loading />}
          </Paper>
        </Grid>
        <Grid item xs={12} md={6} lg={6}>
          <Paper
            elevation="false"
            style={{ position: "fixed", top: "46%", width: "100%" }}
          >
            <ActivityDashboardBarGraph />
          </Paper>
        </Grid>
      </Grid>
    </div>
  );
}
