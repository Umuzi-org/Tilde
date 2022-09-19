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
import { Typography, Button } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";
import orange from "@material-ui/core/colors/orange";
import green from "@material-ui/core/colors/green";
import red from "@material-ui/core/colors/red";
import blue from "@material-ui/core/colors/blue";

const useStyles = makeStyles((theme) => ({
  legend: {
    padding: theme.spacing(1),
  },
}));

export default ({ burnDownSnapshots }) => {
  const [metricFilter, setMetricFilter] = useState("");
  console.log(burnDownSnapshots);
  burnDownSnapshots.map(
    (burnDownSnapshot) =>
      (burnDownSnapshot.timestamp = new Date(burnDownSnapshot.timestamp)
        .toISOString()
        .slice(0, 10))
  );

  const classes = useStyles();
  return (
    <React.Fragment>
      <Typography variant="h6" component="h2">
        Burndown
      </Typography>
      <Typography variant="h6" component="h1">
        Filter by:
        <Button onClick={() => setMetricFilter("TotalCards")}>
          Total Cards
        </Button>
        <Button onClick={() => setMetricFilter("TotalProjects")}>
          Total Projects
        </Button>
        <Button onClick={() => setMetricFilter("CompletedCards")}>
          Completed Cards
        </Button>
        <Button onClick={() => setMetricFilter("CompletedProjects")}>
          Completed Projects
        </Button>
        <Button onClick={() => setMetricFilter("")}>
          Clear Filter
        </Button>
      </Typography>
      <ResponsiveContainer height={500} width="80%">
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
