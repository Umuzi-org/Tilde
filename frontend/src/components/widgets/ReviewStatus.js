import React from "react";
// import TrendingUpIcon from "@material-ui/icons/TrendingUp";
import Chip from "@mui/material/Chip";

import { makeStyles } from "@mui/material/styles";


const statusLabels = {  
    NYC : "not yet competent",
    C : "competent",
    R : "red flag",
    E : "excellent"

}

const useStyles = makeStyles((theme) => {
  return {
    chip: {
      margin: theme.spacing(0.3),
    },
  };
});

export default ({ status }) => {
  const classes = useStyles();
  return (
    <Chip
      className={classes.chip}
    //   icon={<TrendingUpIcon />}
      label={statusLabels[status]}
    />
  );
};
