import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import {
  Paper,
  Typography,
  Tooltip,
  Table,
  TableBody,
  TableRow,
  TableCell,
  IconButton,
} from "@material-ui/core";
import CardReviewBadges from "../../../widgets/CardReviewBadges";
// import CardButton from "../../../widgets/CardButton";
import MoreIcon from "@material-ui/icons/More";

import {
  AGILE_CARD_STATUS_CHOICES,
  BLOCKED,
  READY,
  IN_PROGRESS,
  REVIEW_FEEDBACK,
  IN_REVIEW,
  COMPLETE,
} from "../../../../constants";

import yellow from "@material-ui/core/colors/yellow";
import orange from "@material-ui/core/colors/orange";
import green from "@material-ui/core/colors/green";
import red from "@material-ui/core/colors/red";
import grey from "@material-ui/core/colors/grey";
import blue from "@material-ui/core/colors/blue";

const useStyles = makeStyles((theme) => {
  const card = {
    // borderWidth: 3,
    borderRadius: theme.spacing(2),
    // margin: theme.spacing(1),
    textAlign: "center",
  };
  return {
    root: {
      margin: theme.spacing(1),
      width: theme.spacing(40),
      //   height: theme.spacing(16),
    },

    [BLOCKED]: { ...card, backgroundColor: grey[400] },
    [READY]: { ...card, backgroundColor: blue[400] },
    [IN_PROGRESS]: { ...card, backgroundColor: green[400] },
    [REVIEW_FEEDBACK]: { ...card, backgroundColor: red[400] },
    [IN_REVIEW]: { ...card, backgroundColor: orange[400] },
    [COMPLETE]: { ...card, backgroundColor: yellow[400] },

    row: {
      padding: 5,
    },
  };
});

const TimesTable = ({ card }) => {
  const classes = useStyles();
  const nice = (dateTime) => {
    if (dateTime) {
      const date = new Date(Date.parse(dateTime));
      return new Intl.DateTimeFormat().format(date);
    }
  };

  return (
    <Table size="small">
      <TableBody>
        <TableRow className={classes.row}>
          <TableCell>Due</TableCell>
          <TableCell>{nice(card.dueTime)}</TableCell>
        </TableRow>
        <TableRow className={classes.row}>
          <TableCell>Start</TableCell>
          <TableCell>{nice(card.startTime)}</TableCell>
        </TableRow>
        <TableRow className={classes.row}>
          <TableCell>Review Request</TableCell>
          <TableCell>{nice(card.reviewRequestTime)}</TableCell>
        </TableRow>
        <TableRow className={classes.row}>
          <TableCell>Complete</TableCell>
          <TableCell>{nice(card.completeTime)}</TableCell>
        </TableRow>
      </TableBody>
    </Table>
  );
};

export default ({ card, handleClickOpenCardDetails }) => {
  const classes = useStyles();
  const title = `${card.title} - ${card.assigneeNames.join(", ")}`;
  return (
    <Tooltip title={title}>
      <Paper variant="outlined" className={classes.root}>
        <Table size="small">
          <TableBody>
            <TableRow>
              <TableCell>
                <IconButton onClick={handleClickOpenCardDetails}>
                  <MoreIcon />
                </IconButton>
              </TableCell>
              <TableCell>
                <Paper className={classes[card.status]} variant="outlined">
                  <Typography>
                    {AGILE_CARD_STATUS_CHOICES[card.status]}
                  </Typography>
                </Paper>
              </TableCell>
              <TableCell>
                <CardReviewBadges card={card} />
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
        <TimesTable card={card} />
      </Paper>
    </Tooltip>
  );
};
