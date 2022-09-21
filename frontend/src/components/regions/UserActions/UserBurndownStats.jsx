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
    backgroundColor: "green",
  },
}));

export default ({ burnDownSnapshots }) => {
  const [metricFilter, setMetricFilter] = useState("");
  const [userFilter, setUserFilter] = useState([]);
  burnDownSnapshots.map(
    (burnDownSnapshot) =>
      (burnDownSnapshot.timestamp = new Date(burnDownSnapshot.timestamp)
        .toISOString()
        .slice(0, 10))
  );

  const users = [];
  burnDownSnapshots.forEach((snapshot) => {
    if (users.indexOf(snapshot.user) === -1) {
      users.push(snapshot.user);
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
          onClick={() => setMetricFilter("TotalCards")}
          variant="outlined"
          className={
            metricFilter === "TotalCards" ? classes.selectedFilter : ""
          }
        >
          Total Cards
        </Button>
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
        <Button onClick={() => setMetricFilter("")} variant="outlined">
          Clear Filter
        </Button>
      </Typography>
      <Typography variant="h6" component="h2">
        Filter by user:{" "}
        {users.map((user) => (
          <Button
            key={user}
            onClick={() => setUserFilter(user)}
            variant="outlined"
            className={
              userFilter === user ? classes.selectedFilter : ""
            }
          >
            {user}
          </Button>
        ))}
        <Button onClick={() => setUserFilter("")} variant="outlined">
          Clear Filter
        </Button>
      </Typography>
      <ResponsiveContainer height={500} width="100%">
        <LineChart data={burnDownSnapshots}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="timestamp" interval="preserveEnd" />
          <YAxis />
          <Tooltip />
          <Legend className={classes.legend} />
          {metricFilter === "TotalCards" || metricFilter === "" ? (
            <Line
              type="monotone"
              dataKey="cardsTotalCount"
              name="Total Cards"
              stroke={orange[400]}
              activeDot={{ r: 8 }}
            />
          ) : null}
          {metricFilter === "TotalProjects" || metricFilter === "" ? (
            <Line
              type="monotone"
              dataKey="projectCardsTotalCount"
              name="Total Project Cards"
              stroke={green[400]}
            />
          ) : null}
          {metricFilter === "CompletedCards" || metricFilter === "" ? (
            <Line
              type="monotone"
              dataKey="cardsInCompleteColumnTotalCount"
              name="Completed Cards"
              stroke={blue[400]}
            />
          ) : null}
          {metricFilter === "CompletedProjects" || metricFilter === "" ? (
            <Line
              type="monotone"
              dataKey="projectCardsInCompleteColumnTotalCount"
              name="Completed Project Cards"
              stroke={red[400]}
            />
          ) : null}
        </LineChart>
      </ResponsiveContainer>
    </React.Fragment>
  );
};
