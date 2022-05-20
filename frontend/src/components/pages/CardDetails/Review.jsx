import React, { useState } from "react";
import { makeStyles } from "@material-ui/core/styles";
import Card from "@material-ui/core/Card";
import CardHeader from "@material-ui/core/CardHeader";
import CardContent from "@material-ui/core/CardContent";
import IconButton from "@material-ui/core/IconButton";
import Typography from "@material-ui/core/Typography";
import ReviewStatus from "../../widgets/ReviewStatus";
import ReviewValidationIcons from "../../widgets/ReviewValidationIcons";
import { trimReviewComments } from "./utils";
import Button from "@material-ui/core/Button";
import ReviewPopUp from "./ReviewPopUp";

const useStyles = makeStyles(() => ({
  root: {
    maxWidth: "100%",
  },
  iconAlignment: {},
  timeFont: {
    fontSize: "11px",
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
  iconColor: {
    color: "black",
  },
  cardContent: {
    paddingTop: 0,
    paddingBottom: 0,
  },
  readMoreStyle: {
    textTransform: "none",
    paddingRight: "5px",
  },
  footer: {
    paddingTop: 0,
    "&:last-child": {
      paddingTop: 0,
    },
  },
}));

export default function Review({ review }) {
  const classes = useStyles();
  const [openReviewPopUp, setOpenReviewPopUp] = useState(false);

  const timestamp = new Date(review.timestamp);
  const onClose = () => setOpenReviewPopUp(false) 

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
        <Typography noWrap>{trimReviewComments(review.comments)}</Typography>
        <Button
          type="button"
          size="small"
          className={classes.iconAlignment}
          onClick={() => setOpenReviewPopUp(true)}
        >
          <Typography variant="caption" className={classes.readMoreStyle}>
            ... Read more
          </Typography>
        </Button>
      </CardContent>
      <IconButton disabled>
        <ReviewStatus status={review.status} />
      </IconButton>
      <IconButton disabled className={classes.iconColor}>
        <ReviewValidationIcons review={review} />
      </IconButton>
        <ReviewPopUp
          onClose={onClose}
          openReviewPopUp={openReviewPopUp}
          setOpenReviewPopUp={setOpenReviewPopUp}
          review={review}
        ></ReviewPopUp>
    </Card>
  );
}
