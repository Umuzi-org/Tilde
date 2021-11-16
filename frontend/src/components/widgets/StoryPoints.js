import React from "react";
import TrendingUpIcon from "@mui/icons-material/TrendingUp";
import { Chip, Tooltip } from "@mui/material";

import { makeStyles } from "@mui/material/styles";

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
    <Tooltip title="Story points: is a measure of how much effort this task should take to complete. If one project has storypoints=1 and another one has story points=3 then the second project should take 3 times the effort of the first one">
      <Chip
        className={classes.chip}
        icon={<TrendingUpIcon />}
        label={storyPoints}
      />
    </Tooltip>
  );
};
