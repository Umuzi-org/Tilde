import React from "react";
import { Chip, Tooltip } from "@mui/material";
import LabelIcon from "@mui/icons-material/Create";

import { makeStyles } from "@mui/material/styles";
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
