import React from "react";

import {
  Table,
  TableBody,
  TableRow,
  TableCell,
  Typography,
  Avatar,
  Tooltip,
} from "@material-ui/core";

import Checkbox from "@material-ui/core/Checkbox";
import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => {
  return {
    reviewer: {
      width: theme.spacing(3),
      height: theme.spacing(3),
    },
  };
});

function ReviewersTable({
  reviewerUsers,
  reviewerUserEmails,
  usersThatReviewedSinceLastReviewRequestEmails,
  usersThatReviewedSinceLastReviewRequest,
}) {
  const classes = useStyles();
  const allEmails = [
    ...reviewerUserEmails,
    ...usersThatReviewedSinceLastReviewRequestEmails,
  ];
  const allIds = [...reviewerUsers, ...usersThatReviewedSinceLastReviewRequest];

  function compare(a, b) {
    if (a.email < b.email) {
      return -1;
    }
    if (a.email > b.email) {
      return 1;
    }
    return 0;
  }

  const allUsers = [];

  allIds.forEach((id, index) => {
    if (allUsers.map((user) => user.userId).includes(id)) return;
    allUsers.push({
      userId: id,
      email: allEmails[index],
    });
  });

  allUsers.sort(compare);

  if (allUsers.length === 0) return <Typography>No reviewers!</Typography>;

  return (
    <Table size="small">
      <TableBody>
        {allUsers.map((user) => {
          return (
            <TableRow>
              <TableCell padding="none">
                <Checkbox
                  checked={usersThatReviewedSinceLastReviewRequest.includes(
                    user.userId
                  )}
                  disabled
                />
              </TableCell>
              <TableCell padding="none">
                {reviewerUsers.includes(user.userId) && (
                  <Tooltip title="this user is an allocated reviewer on this project">
                    <Avatar className={classes.reviewer}>R</Avatar>
                  </Tooltip>
                )}
              </TableCell>
              <TableCell>{user.email}</TableCell>
            </TableRow>
          );
        })}
      </TableBody>
    </Table>
  );
}

export default ReviewersTable;
