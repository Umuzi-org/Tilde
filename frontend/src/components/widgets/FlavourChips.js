import React from "react";
import { Chip, Tooltip } from "@material-ui/core";
import LabelIcon from "@material-ui/icons/Create";

import { makeStyles } from "@material-ui/core/styles";
const useStyles = makeStyles((theme) => {
  return {
    chip: {
      margin: theme.spacing(0.3),
    },
  };
});

export default ({ flavourNames }) => {
  const classes = useStyles();
  return (
    <React.Fragment>
      {flavourNames.map((flavour) => {
        return (
          <Tooltip
            key={flavour}
            title={`Please use the following tool when completing this card: ${flavour}`}
          >
            <Chip
              className={classes.chip}
              icon={<LabelIcon />}
              label={"flavour: " + flavour}
            />
          </Tooltip>
        );
      })}
    </React.Fragment>
  );
};
