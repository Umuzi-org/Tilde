import React from "react";
import TrendingUpIcon from "@material-ui/icons/TrendingUp";
import Chip from "@material-ui/core/Chip";

import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => {
  return {
    chip: {
      margin: theme.spacing(0.3),
    },
  };
});

export default ({ storyPoints }) => {
  const classes = useStyles();
  return (
    <Chip
      className={classes.chip}
      icon={<TrendingUpIcon />}
      label={storyPoints}
    />
  );
};
