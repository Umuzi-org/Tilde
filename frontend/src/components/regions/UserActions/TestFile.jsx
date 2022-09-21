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
  return (
    <Paper>
      {sortedTimestampArray.map((timestamp) => (
        <>
          <Typography variant="h6" className={classes.dateTypography}>
            <TodayIcon className={classes.calendarIcon} />
            {new Date(timestamp).toDateString()}
          </Typography>
          {eventList.map((item) => (
            <>
              {item.timestamp.substring(0, 10) === timestamp && (
                <Paper colors={item.eventColor} timestamp={item.timestamp}>
                  <Grid className={classes.fillerStyles}>
                    <Chip
                      className={classes.labelStyles}
                      style={{ backgroundColor: item.eventColor }}
                      label={item.eventName}
                    />
                    <Paper>
                      <Typography variant="h6" className={classes.title}>
                        {item.title}
                      </Typography>
                      <p>
                        {new Date(item.timestamp)
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
