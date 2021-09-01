import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Card from "@material-ui/core/Card";
import CardHeader from "@material-ui/core/CardHeader";
import CardContent from "@material-ui/core/CardContent";
import CardActions from "@material-ui/core/CardActions";
import IconButton from "@material-ui/core/IconButton";
import Typography from "@material-ui/core/Typography";
import Markdown from "react-markdown";
import ReviewStatus from "../../widgets/ReviewStatus";
import ReviewValidationIcons from "../../widgets/ReviewValidationIcons";

const useStyles = makeStyles((theme) => ({
  root: {
    maxWidth: "100%",
    transition: "transform 0.15s ease-in-out",
    "&:hover": { transform: "scale3d(1.0, 1.0, 1)" },
  },
  time: {
    fontSize: 11,
  },
  cardContent: {
    padding: 0,
    "&:last-child": {
      paddingBottom: 0
    }
  }
}));

const Review = ({ review }) => {
  const classes = useStyles();

  const timestamp = new Date(review.timestamp);

  return (
    <Card className={classes.root}>
      <CardHeader
        title={
          <Typography variant="subtitle2">
            {review.reviewerUserEmail}
          </Typography>
        }
        subheader={
          <Typography className={classes.time}>
            {timestamp.toLocaleString()}
          </Typography>
        }
      />
      <CardContent className={classes.CardContent}>
        <Typography paragraph>
          <Markdown source={review.comments}></Markdown>
        </Typography>
      </CardContent>
      <CardActions disableSpacing>
        <IconButton>
          <ReviewStatus status={review.status} />
        </IconButton>
        <IconButton>
          <ReviewValidationIcons review={review} />
        </IconButton>
      </CardActions>
    </Card>
  );
};

export default Review;
