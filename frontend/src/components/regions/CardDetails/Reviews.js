import React from "react";
import { Paper, Typography, List } from "@mui/material";
import { makeStyles } from "@mui/material/styles";

import CircularProgress from "../../widgets/Loading";

import Review from "./Review";

const useStyles = makeStyles((theme) => ({
  paper: {
    padding: theme.spacing(1, 2, 1),
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
          <List style={{ maxHeight: 200, overflow: "auto" }}>
            {reviews
              .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
              .map((review) => {
                return <Review review={review} key={review.id} />;
              })}
          </List>
        </React.Fragment>
      );
    } else {
      body = <CircularProgress />;
    }
  } else {
    body = <Typography paragraph>{"No reviews yet"}</Typography>;
  }

  return (
    <Paper className={classes.sectionPaper}>
      <Typography variant="h6">Reviews</Typography>
      {body}
    </Paper>
  );
};
