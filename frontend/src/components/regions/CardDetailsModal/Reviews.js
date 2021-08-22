import React from "react";
import {
  Paper,
  Table,
  TableContainer,
  TableHead,
  TableBody,
  TableRow,
  TableCell,
  Typography,
} from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";
import Markdown from "react-markdown";

import ReviewStatus from "../../widgets/ReviewStatus";
import ReviewValidationIcons from "../../widgets/ReviewValidationIcons";

const useStyles = makeStyles((theme) => ({
  paper: {
    padding: theme.spacing(1, 2, 1),
  },

  commentColumn: {
    minWidth: 300,
    maxWidth: 300,
  },

  tableContainer: {
    maxHeight: 200,
  },

  sectionPaper: {
    padding: theme.spacing(1),
    marginBottom: theme.spacing(1),
    maxWidth: "100%",
    maxHeight: "100%",
  },
}));

export default ({ reviewIds, reviews }) => {
  const classes = useStyles();
  let body;
  if (reviewIds.length) {
    if (reviews.length) {
      body = (
        <React.Fragment>
          {reviews.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp)).map((review) => {
            const timestamp = new Date(review.timestamp);
            return (
              <TableRow key={review.id}>
                <TableCell>{timestamp.toLocaleString()}</TableCell>
                <TableCell>
                  <ReviewStatus status={review.status} />
                </TableCell>
                <TableCell>{review.reviewerUserEmail}</TableCell>
                <TableCell className={classes.commentColumn}>
                  <Markdown source={review.comments}></Markdown>
                </TableCell>
                <TableCell>
                  <ReviewValidationIcons review={review} />
                </TableCell>
              </TableRow>
            );
          })}
        </React.Fragment>
      );
    } else {
      body = (
        <TableRow>
          <TableCell colSpan="4">Loading...</TableCell>
        </TableRow>
      );
    }
  } else {
    body = (
      <TableRow>
        <TableCell colSpan="4">No reviews yet</TableCell>
      </TableRow>
    );
  }

  return (
    <Paper className={classes.sectionPaper} variant="outlined">
      <Typography variant="h6">Reviews</Typography>
      <TableContainer className={classes.tableContainer}>
        <Table stickyHeader aria-label="sticky table">
          <TableHead>
            <TableRow>
              <TableCell>timestamp</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>reviewer</TableCell>
              <TableCell>Comments</TableCell>
              <TableCell></TableCell>
            </TableRow>
          </TableHead>
          <TableBody>{body}</TableBody>
        </Table>
      </TableContainer>
    </Paper>
  );
};

