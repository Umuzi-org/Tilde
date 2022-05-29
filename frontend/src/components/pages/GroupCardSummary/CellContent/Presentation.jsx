import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import CardStatusChip from "../../../widgets/CardStatusChip.js";

import {
  Paper,
  Tooltip,
  Table,
  TableBody,
  TableRow,
  TableCell,
  IconButton,
} from "@material-ui/core";
import CardBadges from "../../../widgets/CardBadges";
// import CardButton from "../../../widgets/CardButton";
import MoreIcon from "@material-ui/icons/More";

import { routes } from "../../../../routes";

const useStyles = makeStyles((theme) => {
  return {
    root: {
      margin: theme.spacing(1),
      width: theme.spacing(40),
      //   height: theme.spacing(16),
    },

    row: {
      padding: 5,
    },
  };
});

function TimesTable ({ card }) {
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
                <a
                  href={routes.cardDetails.route.path.replace(
                    ":cardId",
                    card.id
                  )}
                >
                  <IconButton>
                    <MoreIcon />
                  </IconButton>
                </a>
              </TableCell>
              <TableCell>
                <CardStatusChip card={card} />
              </TableCell>
              <TableCell>
                <CardBadges card={card} />
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
        <TimesTable card={card} />
      </Paper>
    </Tooltip>
  );
};
