import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Typography from "@material-ui/core/Typography";
import TodayIcon from "@material-ui/icons/Today";
import Grid from "@material-ui/core/Grid";

const useStyles = makeStyles((theme) => ({
  containerStyles: {
    width: "50%",
    margin: 5,
    border: "1px black solid",
  },

  fillerStyles: {
    height: "100%",
    textAlign: "right",
    display: "flex",
    flexDirection: "row",
  },
  labelStyles: {
    width: 20,
    color: "black",
  },
  content: {
    width: "90%",
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

function LogBar({ color, event, timestamp }) {
  const classes = useStyles();

  const date = new Date(timestamp);

  const colorStyleAccordingToEventType = {
    backgroundColor: color,
  };

  return (
    <Grid>
      <Typography variant="h6" className={classes.dateTypography}>
        <TodayIcon className={classes.calendarIcon} /> {date.toDateString()}
      </Typography>
      <Grid className={classes.containerStyles}>
        <Grid className={classes.fillerStyles}>
          <span
            className={classes.labelStyles}
            style={colorStyleAccordingToEventType}
          />
          <div className={classes.content}>{event}</div>
        </Grid>
      </Grid>
    </Grid>
  );
}

function SortBarAccordingToDate({ eventList }) {
  eventList.sort((action1, action2) =>
    action2.timestamp.localeCompare(action1.timestamp)
  );

  return (
    <div>
      {eventList.map((item) => (
        <LogBar
          color={item.eventColor}
          event={item.eventName}
          timestamp={item.timestamp}
        ></LogBar>
      ))}
    </div>
  );
}

export default ({ eventList }) => {
  return (
    <div>
      <SortBarAccordingToDate eventList={eventList} />
    </div>
  );
};
