import React from "react";
import Chip from "@material-ui/core/Chip";
import LabelIcon from "@material-ui/icons/Label";

import { makeStyles } from "@material-ui/core/styles";
const useStyles = makeStyles((theme) => {
  return {
    chip: {
      margin: theme.spacing(0.3),
    },
  };
});

export default ({ tagNames }) => {
  const classes = useStyles();
  return (
    <React.Fragment>
      {tagNames.map((tag) => {
        return (
          <Chip
            className={classes.chip}
            icon={<LabelIcon />}
            key={tag}
            label={tag}
          />
        );
      })}
    </React.Fragment>
  );
};
