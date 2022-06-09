import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";
import { Typography } from "@material-ui/core";
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
  burnDownSnapshots.map(
    (burnDownSnapshot) =>
      (burnDownSnapshot.timestamp = new Date(burnDownSnapshot.timestamp)
        .toISOString()
        .slice(0, 10))
  );
  const classes = useStyles();
  return (
    <div>
      <Typography variant="h6" component="h2">
        Performace Burndown
      </Typography>
      <LineChart width={1000} height={835} data={burnDownSnapshots}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="timestamp" interval="preserveEnd" />
        <YAxis />
        <Tooltip />
        <Legend className={classes.legend}/>
        <Line
          type="monotone"
          dataKey="cardsTotalCount"
          name="Total Cards"
          stroke={orange[400]}
          activeDot={{ r: 8 }}
        />
        <Line
          type="monotone"
          dataKey="projectCardsTotalCount"
          name="Total Project Cards"
          stroke={green[400]}
        />
        <Line
          type="monotone"
          dataKey="cardsInCompleteColumnTotalCount"
          name="Completed Cards"
          stroke={blue[400]}
        />
        <Line
          type="monotone"
          dataKey="projectCardsInCompleteColumnTotalCount"
          name="Completed Project Cards"
          stroke={red[400]}
        />
      </LineChart>
    </div>
  );
};
