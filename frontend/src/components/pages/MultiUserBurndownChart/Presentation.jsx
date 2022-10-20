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
import red from "@material-ui/core/colors/red";

const useStyles = makeStyles((theme) => ({
  legend: {
    padding: theme.spacing(1),
  },
  selectedFilter: {
    color: "green",
    marginRight: "1em"
  },
  unselectedFilter: {
    marginRight: "1em"
  }
}));

function Presentation({ userSnapshotArray, authedUser }){
  const [metricFilter, setMetricFilter] = useState("TotalProjects");
  console.log(userSnapshotArray);
  const classes = useStyles();
  return (
    <React.Fragment>
      <Typography variant="h6" component="h2">
        Burndown
      </Typography>
      <Typography variant="h6" component="h1">
        Filter Metric:{" "}
        <Button
          onClick={() => setMetricFilter("TotalProjects")}
          variant="outlined"
          className={
            metricFilter === "TotalProjects" ? classes.selectedFilter : classes.unselectedFilter
          }
        >
          Total Projects
        </Button>
        <Button
          onClick={() => setMetricFilter("CompletedCards")}
          variant="outlined"
          className={
            metricFilter === "CompletedCards" ? classes.selectedFilter : classes.unselectedFilter
          }
        >
          Completed Cards
        </Button>
        <Button
          onClick={() => setMetricFilter("CompletedProjects")}
          variant="outlined"
          className={
            metricFilter === "CompletedProjects" ? classes.selectedFilter : classes.unselectedFilter
          }
        >
          Completed Projects
        </Button>
      </Typography>
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
              {metricFilter === "TotalProjects" || metricFilter === "" ? (
                <>
                  {userSnapshotArray.map((userOnTeam) => (
                    <Line
                      type="monotone"
                      data={userOnTeam.snapshot}
                      dataKey="projectCardsTotalCount"
                      name={`${userOnTeam.userEmail}`}
                      stroke={userOnTeam.user === authedUser ? green[400] : red[400]}
                      activeDot={{ r: 8 }}
                      key={userOnTeam.user}
                    />
                  ))}
                </>
              ) : null}
              {metricFilter === "CompletedCards" || metricFilter === "" ? (
                <>
                  {userSnapshotArray.map((userOnTeam) => (
                    <Line
                      type="monotone"
                      data={userOnTeam.snapshot}
                      dataKey="cardsInCompleteColumnTotalCount"
                      name={`${userOnTeam.userEmail}`}
                      stroke={userOnTeam.user === authedUser ? green[400] : red[400]}
                      activeDot={{ r: 8 }}
                      key={userOnTeam.user}
                    />
                  ))}
                </>
              ) : null}
              {metricFilter === "CompletedProjects" || metricFilter === "" ? (
                <>
                  {userSnapshotArray.map((userOnTeam) => (
                    <Line
                      type="monotone"
                      data={userOnTeam.snapshot}
                      dataKey="projectCardsInCompleteColumnTotalCount"
                      name={`${userOnTeam.userEmail}`}
                      stroke={userOnTeam.user === authedUser ? green[400] : red[400]}
                      activeDot={{ r: 8 }}
                      key={userOnTeam.user}
                    />
                  ))}
                </>
              ) : null}
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
};

export default Presentation;
