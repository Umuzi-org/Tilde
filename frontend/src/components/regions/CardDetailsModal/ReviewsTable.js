import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import ReviewCard from "./Reviews";

const useStyles = makeStyles({
  root: {
    minWidth: false
  },
});

export default function ReviewsTable() {
  const classes = useStyles();

  return (
    <div className={classes.root}>
      <ReviewCard />
      <ReviewCard />
      <ReviewCard />
    </div>
  );
}
