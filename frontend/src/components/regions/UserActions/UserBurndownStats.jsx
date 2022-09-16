import React from "react";
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
import { Typography } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";
import orange from "@material-ui/core/colors/orange";
import green from "@material-ui/core/colors/green";
import red from "@material-ui/core/colors/red";
import blue from "@material-ui/core/colors/blue";
import {updateBurnDownSnapshots} from "./utils";

const useStyles = makeStyles((theme) => ({
  legend: {
    padding: theme.spacing(1),
  },
}));

export default ({ burnDownSnapshots }) => {
  burnDownSnapshots = burnDownSnapshots.reduce((unique, o) => {
    if (!unique.some((obj) => obj.timestamp === o.timestamp)) {
      unique.push(o);
    }
    return unique;
  }, []);

  burnDownSnapshots.map(
    (burnDownSnapshot) =>
      (burnDownSnapshot.timestamp = new Date(burnDownSnapshot.timestamp)
        .toISOString()
        .slice(0, 10))
  );

  const filterStartDate = new Date();
  filterStartDate.setDate(filterStartDate.getDate() - 21);
  
  const updatedBurnDownSnapshots = updateBurnDownSnapshots({
    burnDownSnapshots,
    filterStartDate,
  });
 
  const classes = useStyles();
  return (
    <React.Fragment>
      <Typography variant="h6" component="h2">
        Burndown
      </Typography>
      <ResponsiveContainer height={500} width="100%">
        <LineChart data={updatedBurnDownSnapshots}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="timestamp" interval="preserveEnd" />
          <YAxis />
          <Tooltip />
          <Legend className={classes.legend} />
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
      </ResponsiveContainer>
    </React.Fragment>
  );
};
