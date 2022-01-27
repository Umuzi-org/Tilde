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
const GetMinimumAndMaximumValue = ({allUsersData}) => {
  const numbersArr = [];
  for(let i in allUsersData){
    allUsersData[i].map((arrValues) => (numbersArr.push(arrValues.COMPETENCE_REVIEW_DONE)));
  }
  const minValue = Math.min(...numbersArr);
  const maxValue = Math.max(...numbersArr);
  return [minValue, maxValue];
}
const ReviewLineChart = ({ data, allUsersData }) => {
  const minAndMaxArr = GetMinimumAndMaximumValue(allUsersData={allUsersData})
  return (
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
      <XAxis dataKey="date" />
      <YAxis domain={[minAndMaxArr[0], minAndMaxArr[1]]} />
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
  );
};

export default ({ team, activityLogDayCounts, eventTypes }) => {
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
                            allUsersData={activityLogDayCounts}
                            eventTypes={eventTypes}
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
