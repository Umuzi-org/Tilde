import React from "react";
import Typography from "@material-ui/core/Typography";
import Paper from "@material-ui/core/Paper";
import TodayIcon from "@material-ui/icons/Today";
import Chip from "@material-ui/core/Chip";
import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => ({
  paper: {
    width: "50rem",
    ["@media (max-width:620px)"]: { // eslint-disable-line no-useless-computed-key
      fontSize: "1rem",
    },
  },
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
  },
  calendarIcon: {
    margin: theme.spacing(1),
  },
  dateTypography: {
    marginTop: theme.spacing(2),
  },
}));

export default function ActivityLog({ eventList, orderedDates }) {
  const classes = useStyles();
  return (
    <React.Fragment>
      {orderedDates.map((timestamp) => (
        <Paper className={classes.paper}>
          <Typography variant="h6" className={classes.dateTypography}>
            <TodayIcon className={classes.calendarIcon} />
            {new Date(timestamp.substring(0, 10)).toDateString()}
          </Typography>
          {eventList.reverse().map((item) => (
            <>
              {item.timestamp.substring(0, 10) ===
                timestamp.substring(0, 10) && (
                <Paper colors={item.eventColor} timestamp={item.timestamp}>
                  <p className={classes.time}>
                    {new Date(item.timestamp).toTimeString().substring(0, 8)}
                  </p>
                  <Typography variant="h6" className={classes.title}>
                    {item.object1Summary.title}
                  </Typography>
                  <Paper className={classes.filler}>
                    <Chip
                      className={classes.label}
                      style={{ backgroundColor: item.eventColor }}
                      label={item.eventName.split("_").join(" ").toLowerCase()}
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
