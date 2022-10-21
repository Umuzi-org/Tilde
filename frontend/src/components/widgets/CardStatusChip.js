import React from "react";
import { Paper, Typography } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";

import {
  AGILE_CARD_STATUS_CHOICES,
  BLOCKED,
  READY,
  IN_PROGRESS,
  REVIEW_FEEDBACK,
  IN_REVIEW,
  COMPLETE,
} from "../../constants";
import { cardColors } from "../../colors";
const useStyles = makeStyles((theme) => {
  const card = {
    margin: theme.spacing(0.3),
    width: theme.spacing(15),
    padding: theme.spacing(0.5),
    borderRadius: theme.spacing(2),
    textAlign: "center",
    [theme.breakpoints.down("md")]: {
      margin: theme.spacing(0.3),
      width: theme.spacing(12),
      padding: theme.spacing(0),
      borderRadius: theme.spacing(6),
      textAlign: "center",
      fontSize: "0.9rem",
    },
  };
  return {
    [BLOCKED]: { ...card, backgroundColor: cardColors.B },
    [READY]: { ...card, backgroundColor: cardColors.R },
    [IN_PROGRESS]: { ...card, backgroundColor: cardColors.IP },
    [REVIEW_FEEDBACK]: { ...card, backgroundColor: cardColors.RF },
    [IN_REVIEW]: { ...card, backgroundColor: cardColors.IR },
    [COMPLETE]: { ...card, backgroundColor: cardColors.C },
  };
});

export default ({ card }) => {
  const classes = useStyles();
  return (
    <Paper className={classes[card.status]} variant="outlined">
      <Typography>{AGILE_CARD_STATUS_CHOICES[card.status]}</Typography>
    </Paper>
  );
};
