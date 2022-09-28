import React from "react";
import Typography from "@material-ui/core/Typography";
import Paper from "@material-ui/core/Paper";
import TodayIcon from "@material-ui/icons/Today";
import Chip from "@material-ui/core/Chip";
import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => ({
  time: {
    marginLeft: theme.spacing(2),
  },
  filler: {
    marginTop: theme.spacing(2),
  },
  label: {
    marginBottom: theme.spacing(2),
    marginLeft: theme.spacing(2),
  },
  title: {
    marginTop: theme.spacing(2),
    marginLeft: theme.spacing(2),

    ["@media (max-width:620px)"]: {
      fontSize: "1rem",
    },
  },
  calendarIcon: {
    margin: theme.spacing(1),
  },
  dateTypography: {
    marginTop: theme.spacing(2),
    ["@media (max-width:620px)"]: {
      fontSize: "1rem",
    },
  },
}));

export default function ActivityLog({ eventList, sortedTimestampArray }) {
  const classes = useStyles();
  return (
    <React.Fragment>
      {sortedTimestampArray.map((timestamp) => (
        <Paper>
          <Typography variant="h6" className={classes.dateTypography}>
            <TodayIcon className={classes.calendarIcon} />
            {new Date(timestamp).toDateString()}
          </Typography>
          {eventList.map((item) => (
            <>
              {item.timestamp.substring(0, 10) === timestamp && (
                <Paper colors={item.eventColor} timestamp={item.timestamp}>
                  <p className={classes.time}>
                    {new Date(item.timestamp).toTimeString().substring(0, 8)}
                  </p>
                  <Typography variant="h6" className={classes.title}>
                    {item.title}
                  </Typography>
                  <Paper className={classes.filler}>
                    <Chip
                      className={classes.label}
                      style={{ backgroundColor: item.eventColor }}
                      label={item.eventName}
                    />
                  </Paper>
                </Paper>
              )}
            </>
          ))}
        </Paper>
      ))}
    </React.Fragment>
  );
}
