import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Grid from "@material-ui/core/Grid";

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

function sortByDates(data) {
  data.sort((action1, action2) => action2.timestamp - action1.timestamp);
}
function LogBar({ color, event }) {
  const classes = useStyles();
  const adjustStyle = {
    backgroundColor: color,
  };
  return (
    <Grid className={classes.containerStyles}>
      <Grid className={classes.fillerStyles}>
        <span className={classes.labelStyles} style={adjustStyle} />
        <div className={classes.content}>
          <div>{event}</div>
          {/* <div>{object1ContentTypeName}</div> */}
        </div>
      </Grid>
    </Grid>
  );
}
export default ({ three }) => {
  // console.log(sortByDates("xx", three));
  return (
    <div>
      {three.map((item) => (
        <LogBar
          color={item.eventColor}
          event={item.eventName}
          object1ContentTypeName={item.object1ContentTypeName}
        />
      ))}
    </div>
  );
};
