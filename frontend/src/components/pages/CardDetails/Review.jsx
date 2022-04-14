import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Card from "@material-ui/core/Card";
import CardHeader from "@material-ui/core/CardHeader";
import CardContent from "@material-ui/core/CardContent";
import IconButton from "@material-ui/core/IconButton";
import Typography from "@material-ui/core/Typography";
import Markdown from "react-markdown";
import ReviewStatus from "../../widgets/ReviewStatus";
import ReviewValidationIcons from "../../widgets/ReviewValidationIcons";

const useStyles = makeStyles((theme) => ({
  root: {
    maxWidth: "100%",
  },
  timeFont: {
    fontSize: 11,
  },
  reviewerFont: {
    fontSize: "100%",
    fontWeight: "bold",
  },
  cardFont: {
    fontSize: "100%",
  },
  cardHeader: {
    paddingBottom: 0,
    "&:last-child": {
      paddingBottom: 0,
    },
  },
  cardContent: {
    paddingTop: 0,
    paddingBottom: 0,
  },
  footer: {
    paddingTop: 0,
    "&:last-child": {
      paddingTop: 0,
    },
  },
}));

export default function Review({ review }){
  const classes = useStyles();

  const timestamp = new Date(review.timestamp);

  return (
    <Card className={classes.root} variant="outlined">
      <CardHeader
        title={
          <Typography className={classes.timeFont}>
            {timestamp.toLocaleString()}
          </Typography>
        }
        subheader={
          <Typography className={classes.reviewerFont}>
            {review.reviewerUserEmail}
          </Typography>
        }
        className={classes.cardHeader}
      />
      <CardContent className={classes.cardContent}>
        <Markdown children={review.comments} />
      </CardContent>
      <IconButton>
        <ReviewStatus status={review.status} />
      </IconButton>
      <IconButton>
        <ReviewValidationIcons review={review} />
      </IconButton>
    </Card>
  );
};
