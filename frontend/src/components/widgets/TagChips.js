import React from "react";
import { Chip, Tooltip } from "@material-ui/core";
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
          <Tooltip
            key={tag}
            title={`Completing this card will move you towards your ${tag} goals`}
          >
            <Chip className={classes.chip} icon={<LabelIcon />} label={tag} />
          </Tooltip>
        );
      })}
    </React.Fragment>
  );
};
