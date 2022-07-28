import React from "react";
// import { Paper, Grid } from "@material-ui/core";
import Paper from "@material-ui/core/Paper";
import Grid from "@material-ui/core/Grid";

export default ({ activityLog }) => {
  return (
    <Paper>
      <Grid container>
        <Grid>
          {/* <Plot
            data={activityLog.map((trace) => {
              return { ...trace, type: "bar" };
            })}
            layout={{ barmode: "group", width: "100%" }}
          /> */}
        </Grid>

        <Grid>
          {activityLog[0].x.reverse().map((date, index) => {
            return (
              <div>
                {date}

                {activityLog.map((trace) => {
                  return (
                    <div>
                      {trace.name}
                      {trace.y[index]}
                      {trace.meta[index]}
                    </div>
                  );
                })}
              </div>
            );
          })}
        </Grid>
      </Grid>
    </Paper>
  );
};
