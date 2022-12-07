import React, { useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import Typography from "@material-ui/core/Typography";
import Button from "@material-ui/core/Button";
import Grid from "@material-ui/core/Grid";
import { makeStyles } from "@material-ui/core/styles";
import green from "@material-ui/core/colors/green";

const useStyles = makeStyles((theme) => ({
  legend: {
    padding: theme.spacing(1),
  },
  selectedFilter: {
    color: "green",
    marginRight: "1em",
  },
  unselectedFilter: {
    marginRight: "1em",
  },
}));

function Presentation({
  userSnapshotArray,
  metrics,
  metricFilter,
  handleChangeMetricFilter,
}) {
  const classes = useStyles();
  return (
    <React.Fragment>
      {Object.keys(metrics).map((metric) => (
        <Button
          onClick={() => handleChangeMetricFilter(metric)}
          variant="outlined"
          size="small"
          className={
            metricFilter === metric
              ? classes.selectedFilter
              : classes.unselectedFilter
          }
        >
          {metrics[metric]}
        </Button>
      ))}
      <Grid container>
        <Grid item xs={10}>
          <ResponsiveContainer height={500} width="100%">
            <LineChart>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                dataKey="timestamp"
                interval="preserveEnd"
                allowDuplicatedCategory={false}
              />
              <YAxis />
              <Tooltip />
              <Legend className={classes.legend} />
              {userSnapshotArray.map((userOnTeam) => (
                <Line
                  type="monotone"
                  data={userOnTeam.snapshot}
                  dataKey={metricFilter}
                  name={`${userOnTeam.userEmail}`}
                  stroke={green[400]}
                  activeDot={{ r: 8 }}
                  strokeWidth={1}
                  dot={false}
                  key={userOnTeam.user}
                />
              ))}
            </LineChart>
          </ResponsiveContainer>
        </Grid>
        <Grid item xs={2}>
          <Typography variant="h6" component="h2">
            Cohort users
          </Typography>
          {userSnapshotArray.map((userOnTeam) => (
            <Grid item key={userOnTeam.user}>
              <Typography>{userOnTeam.userEmail}</Typography>
            </Grid>
          ))}
        </Grid>
      </Grid>
    </React.Fragment>
  );
}

export default Presentation;
