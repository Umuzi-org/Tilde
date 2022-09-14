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

const timestampArray = ["2022-09-02T13:46:16.295020Z", "2022-09-05T10:46:16.221191Z", "2022-09-01T13:18:03.743668Z"];

function LogBar({ color, event, timestamp }) {
  const classes = useStyles();
  console.log(timestamp);
  const date = new Date(timestamp);

  const colorStyleAccordingToEventType = {
    backgroundColor: color,
  };

  return (
    <Grid>
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
  const classes = useStyles();
  return (
    <div>
      {timestampArray.map((timestamp) => (
        <>
          <Typography variant="h6" className={classes.dateTypography}>
            <TodayIcon className={classes.calendarIcon} /> {timestamp}
          </Typography>
          {eventList.map((item) => (
            <>
              {item.timestamp === timestamp && (
                <LogBar
                  color={item.eventColor}
                  event={item.eventName}
                  timestamp={item.timestamp}
                ></LogBar>
              )}
            </>
          ))}
        </>
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
