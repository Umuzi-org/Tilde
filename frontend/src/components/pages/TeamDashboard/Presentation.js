import React from "react";
import {
  Grid,
  Paper,
  Table,
  TableBody,
  TableRow,
  TableCell,
  Typography,
} from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";

import {
  ACTIVITY_LOG_EVENT_TYPE_COMPETENCE_REVIEW_DONE,
  ACTIVITY_LOG_EVENT_TYPE_PR_REVIEWED,
} from "../../../constants";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from "recharts";

const useStyles = makeStyles((theme) => ({
  paper: {
    padding: theme.spacing(1),
    margin: theme.spacing(1),
    textAlign: "center",
    color: theme.palette.text.secondary,
  },
}));

const ReviewLineChart = ({
  data,
  minimumCount,
  maximumCount,
  minimumDate,
  maximumDate,
}) => {
  // TODO calculate maximum and minimum so that all the graphs have the same proportions
  return (
    // <ResponsiveContainer width="100%" height="100%">
    <LineChart
      width={900}
      height={100}
      data={data}
      margin={{
        top: 5,
        right: 30,
        left: 20,
        bottom: 5,
      }}
    >
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis
        dataKey="date"
        domain={[
          Math.floor(new Date(minimumDate).getTime() / 1000),
          Math.floor(new Date(maximumDate).getTime() / 1000),
        ]}
      />
      <YAxis domain={[minimumCount, maximumCount]} />
      <Tooltip />
      <Line
        type="monotone"
        dataKey={ACTIVITY_LOG_EVENT_TYPE_COMPETENCE_REVIEW_DONE}
        stroke="#8884d8"
        activeDot={{ r: 8 }}
      />
      <Line
        type="monotone"
        dataKey={ACTIVITY_LOG_EVENT_TYPE_PR_REVIEWED}
        stroke="#82ca9d"
      />
    </LineChart>
    // </ResponsiveContainer>
  );
};

export default ({
  team,
  activityLogDayCounts,
  eventTypes,
  minimumDate,
  maximumDate,
}) => {
  const classes = useStyles();
  if (team)
    return (
      <React.Fragment>
        <Grid container spacing={1}>
          <Grid item xs={12}>
            <Paper className={classes.paper}>
              <Table>
                <TableBody>
                  {team.members.map((member) => (
                    <TableRow key={member.userId}>
                      <TableCell>
                        <Typography>{member.userEmail}</Typography>
                      </TableCell>
                      <TableCell>
                        {activityLogDayCounts ? (
                          <ReviewLineChart
                            data={activityLogDayCounts[member.userId]}
                            eventTypes={eventTypes}
                            minimumDate={minimumDate}
                            maximumDate={maximumDate}
                          ></ReviewLineChart>
                        ) : (
                          "Loading..."
                        )}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </Paper>
          </Grid>
        </Grid>
      </React.Fragment>
    );
  return <React.Fragment />; // TODO: loading. update story to show this
};
