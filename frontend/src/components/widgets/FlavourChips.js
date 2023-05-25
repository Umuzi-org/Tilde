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

export default ({ flavourNames, variant }) => {
  const classes = useStyles();

  return (
    <React.Fragment>
      {flavourNames.map((flavour) => {
        const props = {};
        if (variant === "small") {
          props.label = flavour;
          props.size = "small";
        } else {
          props.label = "flavour: " + flavour;
          props.icon = <LabelIcon />;
        }

        return (
          <Tooltip
            key={flavour}
            title={`Please use the following tool when completing this card: ${flavour}`}
            {...props}
          >
            <Chip className={classes.chip} {...props} />
          </Tooltip>
        );
      })}
    </React.Fragment>
  );
};
