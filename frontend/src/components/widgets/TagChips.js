import React from "react";
import { Chip, Tooltip } from "@mui/material";
import LabelIcon from "@mui/icons-material/Label";

import { makeStyles } from "@mui/material/styles";
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
