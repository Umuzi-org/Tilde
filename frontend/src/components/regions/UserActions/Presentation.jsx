import React from "react";
import Paper from "@material-ui/core/Paper";
import Grid from "@material-ui/core/Grid";
import Loading from "../../widgets/Loading";
import { makeStyles } from "@material-ui/core/styles";
import DayLog from "./DayLog";
import UserBurnDownChart from "./UserBurndownStats";
import TestFile from "./TestFile";

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
  currentUserBurndownStats,
}) {
  const classes = useStyles();
  console.log("xx", "hello?");
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
        {/* <Grid>
          <TestFile
            eventList={actionLogByDate}
            sortedTimestampArray={orderedDates}
          />
        </Grid> */}
      </Grid>
    </div>
  );
}
