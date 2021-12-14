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
=======
import React from "react";
import yellow from "@material-ui/core/colors/yellow";
import orange from "@material-ui/core/colors/orange";
import green from "@material-ui/core/colors/green";
import red from "@material-ui/core/colors/red";
import grey from "@material-ui/core/colors/grey";
import blue from "@material-ui/core/colors/blue";
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
const useStyles = makeStyles((theme) => {
  const card = {
    margin: theme.spacing(0.3),
    width: theme.spacing(15),
    padding: theme.spacing(0.5),
    borderRadius: theme.spacing(2),
    textAlign: "center",
  };
  return {
    [BLOCKED]: { ...card, backgroundColor: grey[400] },
    [READY]: { ...card, backgroundColor: blue[400] },
    [IN_PROGRESS]: { ...card, backgroundColor: green[400] },
    [REVIEW_FEEDBACK]: { ...card, backgroundColor: red[400] },
    [IN_REVIEW]: { ...card, backgroundColor: orange[400] },
    [COMPLETE]: { ...card, backgroundColor: yellow[400] },
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
