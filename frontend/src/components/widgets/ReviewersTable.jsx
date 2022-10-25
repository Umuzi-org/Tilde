import React from "react";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableRow from "@material-ui/core/TableRow";
import MuiTableCell from "@material-ui/core/TableCell";
import Typography from "@material-ui/core/Typography";
import Avatar from "@material-ui/core/Avatar";
import Tooltip from "@material-ui/core/Tooltip";
import Checkbox from "@material-ui/core/Checkbox";
import { makeStyles, withStyles } from "@material-ui/core/styles";
import UserAvatarLink from "./UserAvatarLink";

const TableCell = withStyles({
  root: {
    borderBottom: "none",
  },
})(MuiTableCell);

const useStyles = makeStyles((theme) => {
  return {
    reviewer: {
      width: theme.spacing(3),
      height: theme.spacing(3),
    },
    table: {
      height: "20vh",
      [theme.breakpoints.down("md")]: {
        maxHeight: "30vh",
      },
      overflow: "auto",
    },
    dates: {
      paddingTop: "6%",
    },
  };
});

export default function ReviewersTable({
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
    <div className={classes.table}>
      <Table size="small">
        <TableBody>
          {allUsers.map((user) => {
            return (
              <TableRow key={user.userId}>
                <TableCell padding="none">
                  <Checkbox
                    size="medium"
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
                <TableCell>
                  <UserAvatarLink email={user.email} userId={user.userId} />
                </TableCell>
              </TableRow>
            );
          })}
        </TableBody>
      </Table>
    </div>
  );
}
