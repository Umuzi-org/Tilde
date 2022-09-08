import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Paper from "@material-ui/core/Paper";
import Grid from "@material-ui/core/Grid";
import ActivityLog from "./ActivityLog";

import { eventTypeColors } from "../../../colors";

const useStyles = makeStyles((theme) => ({
  containerStyles: {
    width: "50%",
    margin: 10,
    border: "1px black solid",
  },

  fillerStyles: {
    height: "100%",
    textAlign: "right",
    // width: "10%",
    display: "flex",
    flexDirection: "row",
  },
  labelStyles: {
    // height: "100%",
    width: 20,
    color: "black",
    // fontWeight: 900,
  },
  content: {
    // height: "100%",
    // padding: 10,
    width: "90%",
  },
}));

function LogBar({ colors, orderedDates, actionLogByDate }) {
  const classes = useStyles();
  const adjustStyle = {
    backgroundColor: colors,
  };
  return (
    <div className={classes.containerStyles}>
      <div className={classes.fillerStyles}>
        <span className={classes.labelStyles} style={adjustStyle} />
        <div className={classes.content}>
          this is where all content goes. All of it here. even more more more
          content. right here!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        </div>
      </div>
    </div>
  );
}

export default function Presentation({ props }) {
  return (
    <div>
      {/* {eventTypeColors.map((color) => ( */}
      <LogBar colors={"red"} />
      {/* ))} */}
    </div>
  );
}
