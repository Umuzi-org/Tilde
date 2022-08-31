import React from "react";
import Paper from "@material-ui/core/Paper";
import Grid from "@material-ui/core/Grid";
import Loading from "../../widgets/Loading";
import { makeStyles } from "@material-ui/core/styles";
import DayLog from "./DayLog";

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
    <div className={classes.column} onScroll={handleScroll}>
      <Grid container>
        <Grid>
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
      </Grid>
    </div>
  );
}
