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
import { Typography, Button, Grid } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";
import orange from "@material-ui/core/colors/orange";
import green from "@material-ui/core/colors/green";
import red from "@material-ui/core/colors/red";
import blue from "@material-ui/core/colors/blue";

const useStyles = makeStyles((theme) => ({
  legend: {
    padding: theme.spacing(1),
  },
  selectedFilter: {
    color: "green",
  },
}));

export default ({ burnDownSnapshots }) => {
  const [metricFilter, setMetricFilter] = useState("TotalProjects");

  burnDownSnapshots.map(
    (burnDownSnapshot) =>
      (burnDownSnapshot.timestamp = new Date(burnDownSnapshot.timestamp)
        .toISOString()
        .slice(0, 10))
  );
  
  const authedUserId = 1
  // seperate the authed user and the other users' snapshots
  const authedUserIdSnapshot = burnDownSnapshots.filter(
    (snapshot) => snapshot.user === authedUserId
  );

  // organize data from the team, and format it so the chart can use it
  const usersOnTeam = [];
  burnDownSnapshots.forEach((snapshot) => {
    if (
      !usersOnTeam.some((user) => user.user === snapshot.user) &&
      snapshot.user !== authedUserId
    ) {
      const userSnapshot = {
        user: snapshot.user,
        userEmail: snapshot.userEmail,
        snapshot: [snapshot],
      };
      usersOnTeam.push(userSnapshot);
    } else if (usersOnTeam.some((user) => user.user === snapshot.user)) {
      const userIndex = usersOnTeam.findIndex((user) => {
        return user.user === snapshot.user;
      });
      usersOnTeam[userIndex].snapshot.push(snapshot);
    }
  });

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
            metricFilter === "TotalProjects" ? classes.selectedFilter : ""
          }
        >
          Total Projects
        </Button>
        <Button
          onClick={() => setMetricFilter("CompletedCards")}
          variant="outlined"
          className={
            metricFilter === "CompletedCards" ? classes.selectedFilter : ""
          }
        >
          Completed Cards
        </Button>
        <Button
          onClick={() => setMetricFilter("CompletedProjects")}
          variant="outlined"
          className={
            metricFilter === "CompletedProjects" ? classes.selectedFilter : ""
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
                data={authedUserIdSnapshot}
                dataKey="timestamp"
                interval="preserveEnd"
                allowDuplicatedCategory={false}
              />
              <YAxis />
              <Tooltip />
              <Legend className={classes.legend} />
              {metricFilter === "TotalProjects" || metricFilter === "" ? (
                <>
                  <Line
                    type="monotone"
                    data={authedUserIdSnapshot}
                    dataKey="projectCardsTotalCount"
                    name={authedUserIdSnapshot[0].userEmail}
                    stroke={green[400]}
                  />
                  {usersOnTeam.map((userOnTeam) => (
                    <Line
                      type="monotone"
                      data={userOnTeam.snapshot}
                      dataKey="projectCardsTotalCount"
                      name={`${userOnTeam.userEmail}`}
                      stroke={orange[400]}
                      activeDot={{ r: 8 }}
                      key={userOnTeam.user}
                    />
                  ))}
                </>
              ) : null}
              {metricFilter === "CompletedCards" || metricFilter === "" ? (
                <>
                  <Line
                    type="monotone"
                    data={authedUserIdSnapshot}
                    dataKey="cardsInCompleteColumnTotalCount"
                    name={authedUserIdSnapshot[0].userEmail}
                    stroke={blue[400]}
                  />
                  {usersOnTeam.map((userOnTeam) => (
                    <Line
                      type="monotone"
                      data={userOnTeam.snapshot}
                      dataKey="cardsInCompleteColumnTotalCount"
                      name={`${userOnTeam.userEmail}`}
                      stroke={orange[400]}
                      activeDot={{ r: 8 }}
                      key={userOnTeam.user}
                    />
                  ))}
                </>
              ) : null}
              {metricFilter === "CompletedProjects" || metricFilter === "" ? (
                <>
                  <Line
                    type="monotone"
                    data={authedUserIdSnapshot}
                    dataKey="projectCardsInCompleteColumnTotalCount"
                    name={authedUserIdSnapshot[0].userEmail}
                    stroke={red[400]}
                  />
                  {usersOnTeam.map((userOnTeam) => (
                    <Line
                      type="monotone"
                      data={userOnTeam.snapshot}
                      dataKey="cardsInCompleteColumnTotalCount"
                      name={`${userOnTeam.userEmail}`}
                      stroke={orange[400]}
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
          {usersOnTeam.map((userOnTeam) => (
            <Grid item key={userOnTeam.user}>
              <Typography>{userOnTeam.userEmail}</Typography>
            </Grid>
          ))}
        </Grid>
      </Grid>
    </React.Fragment>
  );
};
