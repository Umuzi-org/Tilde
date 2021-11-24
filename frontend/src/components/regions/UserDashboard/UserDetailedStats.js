import React from "react";

import {
  Table,
  TableBody,
  TableCell,
  TableRow,
  Typography,
} from "@material-ui/core";

export default ({ detailedStats }) => {
  if (!detailedStats) return <React.Fragment />;
  const detailedStatsData = Object.keys(detailedStats).reduce((obj, k) => Object.assign(obj, { [detailedStats[k.split(/(?=[A-Z])/).join('_').toLowerCase()]]: detailedStats[k] }),{});
  console.log("Bee", detailedStatsData);
  return (
    <Table>
      <TableBody>
        <TableRow>
          <TableCell>
            <Typography variant="h6" component="h2">
              Performance
            </Typography>
          </TableCell>
        </TableRow>
        <TableRow>
          <TableCell>Cards in complete column as assignee</TableCell>
          <TableCell>
            {detailedStats.cardsInCompletedColumnAsAssignee}
          </TableCell>
        </TableRow>
        <TableRow>
          <TableCell>Cards in review column as assignee</TableCell>
          <TableCell>{detailedStats.cardsInReviewColumnAsAssignee}</TableCell>
        </TableRow>
        <TableRow>
          <TableCell>Cards in review feedback column as assignee</TableCell>
          <TableCell>
            {detailedStats.cardsInReviewFeedbackColumnAsAssignee}
          </TableCell>
        </TableRow>
        <TableRow>
          <TableCell>Cards in complete column as assignee</TableCell>
          <TableCell>{detailedStats.cardsInProgressColumnAsAssignee}</TableCell>
        </TableRow>
        <TableRow>
          <TableCell>Cards completed in the last 7 days</TableCell>
          <TableCell>
            {detailedStats.cardsCompletedLast_7DaysAsAssignee}
          </TableCell>
        </TableRow>
        <TableRow>
          <TableCell>Cards started in the last 7 days as assignee</TableCell>
          <TableCell>
            {detailedStats.cardsStartedLast_7DaysAsAssignee}
          </TableCell>
        </TableRow>
        <TableRow>
          <TableCell>Total competence reviews done</TableCell>
          <TableCell>{detailedStats.totalTildeReviewsDone}</TableCell>
        </TableRow>
        <TableRow>
          <TableCell>Total competence reviews done in last 7 days</TableCell>
          <TableCell>{detailedStats.tildeReviewsDoneLast_7Days}</TableCell>
        </TableRow>
        <TableRow>
          <TableCell>Total pull request reviews done</TableCell>
          <TableCell>{detailedStats.totalPrReviewsDone}</TableCell>
        </TableRow>
        <TableRow>
          <TableCell>Total pull request reviews done in last 7 day</TableCell>
          <TableCell>{detailedStats.prReviewsDoneLast_7Days}</TableCell>
        </TableRow>
        <TableRow>
          <TableCell>Tilde cards reviewed in last 7 days</TableCell>
          <TableCell>{detailedStats.tildeCardsReviewedInLast_7Days}</TableCell>
        </TableRow>
      </TableBody>
    </Table>
  );
};
