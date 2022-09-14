import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Grid from "@material-ui/core/Grid";

const useStyles = makeStyles((theme) => ({
  containerStyles: {
    width: "50%",
    margin: 10,
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
  },
}));

function LogBar({ color, event, timestamp }) {
  const classes = useStyles();
  const colorStyleAccordingToEventType = {
    backgroundColor: color,
  };

  return (
    <Grid className={classes.containerStyles}>
      <Grid className={classes.fillerStyles}>
        <span
          className={classes.labelStyles}
          style={colorStyleAccordingToEventType}
        />
        <div className={classes.content}>
          <div>{event}</div>
          <div>{timestamp}</div>
        </div>
      </Grid>
    </Grid>
  );
}
export default ({ eventList }) => {
  eventList.sort((a, b) => b.timestamp.localeCompare(a.timestamp));
  console.log("xx", eventList);
  return (
    <div>
      {eventList.map((item) => (
        <LogBar
          color={item.eventColor}
          event={item.eventName}
          timestamp={item.timestamp}
        />
      ))}
    </div>
  );
};
