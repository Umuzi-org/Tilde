import React from "react";
import TrendingUpIcon from "@material-ui/icons/TrendingUp";
import { Chip, Tooltip } from "@material-ui/core";

import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => {
  return {
    chip: {
      margin: theme.spacing(1),
    },
  };
});

export default ({ storyPoints, variant }) => {
  const classes = useStyles();

  const props = {};
  if (variant === "small") {
    props.size = "small";
  }

  return (
    <Tooltip title="Story points: is a measure of how much effort this task should take to complete. If one project has storypoints=1 and another one has story points=3 then the second project should take 3 times the effort of the first one">
      <Chip
        className={classes.chip}
        icon={<TrendingUpIcon />}
        label={storyPoints}
        {...props}
      />
    </Tooltip>
  );
};
