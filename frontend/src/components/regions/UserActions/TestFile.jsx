import React from "react";
import Typography from "@material-ui/core/Typography";
import Paper from "@material-ui/core/Paper";
import TodayIcon from "@material-ui/icons/Today";
import Chip from "@material-ui/core/Chip";
import Grid from "@material-ui/core/Grid";
import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => ({
  fillerStyles: {
    marginTop: theme.spacing(2),
  },
  labelStyles: {
    color: "black",
  },
  title: {
    marginTop: theme.spacing(2),
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

export default function TestFile({ eventList, sortedTimestampArray }) {
  const classes = useStyles();
  console.log(eventList);
  return (
    <Paper>
      {sortedTimestampArray.map((timestamp) => (
        <>
          <Typography variant="h6" className={classes.dateTypography}>
            <TodayIcon className={classes.calendarIcon} />
            {new Date(timestamp).toDateString()}
          </Typography>
          {Object.keys(eventList).map((item) => (
            <>
              {eventList[item].timestamp.substring(0, 10) === timestamp && (
                <Paper
                  colors={eventList[item].eventColor}
                  timestamp={eventList[item].timestamp}
                >
                  <Grid className={classes.fillerStyles}>
                    <Chip
                      className={classes.labelStyles}
                      style={{ backgroundColor: eventList[item].eventColor }}
                      label={eventList[item].eventName}
                    />
                    <Paper>
                      <Typography variant="h6" className={classes.title}>
                        {eventList[item].title}
                      </Typography>
                      <p>
                        {new Date(eventList[item].timestamp)
                          .toTimeString()
                          .substring(0, 8)}
                      </p>
                    </Paper>
                  </Grid>
                </Paper>
              )}
            </>
          ))}
        </>
      ))}
    </Paper>
  );
}
