import React from "react";
import Paper from "@material-ui/core/Paper";
import Typography from "@material-ui/core/Typography";
import List from "@material-ui/core/List";
import { makeStyles } from "@material-ui/core/styles";

import CircularProgress from "../../widgets/Loading";

import Review from "./Review";

const useStyles = makeStyles((theme) => ({
  sectionPaper: {
    padding: theme.spacing(1),
    marginBottom: theme.spacing(1),
    marginRight: theme.spacing(2),
    width: "99.2%",
    height: "100%",
  },
  list: {
    [theme.breakpoints.down("md")]: {
      maxHeight: "20em",
      overflow: "auto",
    },
  },
}));

export default ({ reviewIds, reviews }) => {
  const classes = useStyles();
  let body;
  if (reviewIds.length) {
    if (reviews.length) {
      body = (
        <React.Fragment>
          <List
            className={classes.list}
            style={{ maxHeight: "30vh", overflow: "auto" }}
          >
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
    <Paper className={classes.sectionPaper} variant={"outlined"}>
      <Typography variant="h6">Reviews:</Typography>
      {body}
    </Paper>
  );
};
