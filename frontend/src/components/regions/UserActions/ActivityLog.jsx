import React from "react";
import Typography from "@material-ui/core/Typography";
import TodayIcon from "@material-ui/icons/Today";
import Grid from "@material-ui/core/Grid";
import { makeStyles } from "@material-ui/core/styles";

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

export default function ActivityLog({ eventList, sortedTimestampArray }) {
  const classes = useStyles();

  return (
    <div>
      {sortedTimestampArray.map((timestamp) => (
        <>
          <Typography variant="h6" className={classes.dateTypography}>
            <TodayIcon className={classes.calendarIcon} />
            {new Date(timestamp).toDateString()}
          </Typography>
          {eventList.map((item) => (
            <>
              {item.timestamp === timestamp && (
                <Grid>
                  <Grid
                    className={classes.containerStyles}
                    colors={item.eventColor}
                    timestamp={item.timestamp}
                  >
                    <Grid className={classes.fillerStyles}>
                      <span
                        className={classes.labelStyles}
                        style={{ backgroundColor: item.eventColor }}
                      />
                      <span className={classes.content}>{item.eventName}</span>
                    </Grid>
                  </Grid>
                </Grid>
              )}
            </>
          ))}
        </>
      ))}
    </div>
  );
}
