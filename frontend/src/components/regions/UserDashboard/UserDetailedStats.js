import React from "react";

import { Table, TableBody, TableCell, TableRow } from "@material-ui/core";

export default ({ detailedStats }) => {
  console.log(detailedStats);
  if (!detailedStats) return <React.Fragment />;
  return (
    <Table>
      <TableBody>
        <TableRow>
          <TableCell>Cards in complete column</TableCell>
          <TableCell>
            {detailedStats.cardsInCompletedColumnAsAssignee}
          </TableCell>
        </TableRow>
        <TableRow>
          <TableCell>Cards in review column</TableCell>
          <TableCell>{detailedStats.cardsInReviewColumnAsAssignee}</TableCell>
        </TableRow>
        <TableRow>
          <TableCell>Cards in review feedback column</TableCell>
          <TableCell>
            {detailedStats.cardsInReviewFeedbackColumnAsAssignee}
          </TableCell>
        </TableRow>
        <TableRow>
          <TableCell>Cards in complete column</TableCell>
          <TableCell>{detailedStats.cardsInProgressColumnAsAssignee}</TableCell>
        </TableRow>
        <TableRow>
          <TableCell>Cards completed in the last 7 days</TableCell>
          <TableCell>
            {detailedStats.cardsCompletedLast_7DaysAsAssignee}
          </TableCell>
        </TableRow>
        <TableRow>
          <TableCell>Cards started in the last 7 days</TableCell>
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
