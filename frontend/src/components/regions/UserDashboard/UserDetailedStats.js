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
            {detailedStats.cards_assigned_with_status_complete}
          </TableCell>
        </TableRow>
        <TableRow>
          <TableCell>Cards in review column as assignee</TableCell>
          <TableCell>{detailedStats.cards_assigned_with_status_in_review}</TableCell>
        </TableRow>
        <TableRow>
          <TableCell>Cards in review feedback column as assignee</TableCell>
          <TableCell>
            {detailedStats.cards_assigned_with_status_review_feedback}
          </TableCell>
        </TableRow>
        <TableRow>
          <TableCell>Cards in progress column as assignee</TableCell>
          <TableCell>{detailedStats.cards_assigned_with_status_in_progress}</TableCell>
        </TableRow>
        <TableRow>
          <TableCell>Cards in blocked column as assignee</TableCell>
          <TableCell>{detailedStats.cards_assigned_with_status_blocked}</TableCell>
        </TableRow>
        <TableRow>
          <TableCell>Cards in ready column as assignee</TableCell>
          <TableCell>{detailedStats.cards_assigned_with_status_ready}</TableCell>
        </TableRow>
        <TableRow>
          <TableCell>Cards completed in the last 7 days</TableCell>
          <TableCell>
            {detailedStats.cards_completed_last_7_days_as_assignee}
          </TableCell>
        </TableRow>
        <TableRow>
          <TableCell>Cards started in the last 7 days as assignee</TableCell>
          <TableCell>
            {detailedStats.cards_started_last_7_days_as_assignee}
          </TableCell>
        </TableRow>
        <TableRow>
          <TableCell>Total tilde reviews done</TableCell>
          <TableCell>{detailedStats.total_tilde_reviews_done}</TableCell>
        </TableRow>
        <TableRow>
          <TableCell>Total tilde reviews done in last 7 days</TableCell>
          <TableCell>{detailedStats.tilde_reviews_done_last_7_days}</TableCell>
        </TableRow>
        <TableRow>
          <TableCell>Total pull request reviews done</TableCell>
          <TableCell>{detailedStats.total_pr_reviews_done}</TableCell>
        </TableRow>
        <TableRow>
          <TableCell>Total pull request reviews done in last 7 day</TableCell>
          <TableCell>{detailedStats.pr_reviews_done_last_7_days}</TableCell>
        </TableRow>
        <TableRow>
          <TableCell>Tilde cards reviewed in last 7 days</TableCell>
          <TableCell>{detailedStats.tilde_cards_reviewed_in_last_7_days}</TableCell>
        </TableRow>
      </TableBody>
    </Table>
  );
};
