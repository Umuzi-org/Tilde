import React, { useState } from "react";
import { makeStyles } from "@material-ui/core/styles";
import Card from "@material-ui/core/Card";
import CardHeader from "@material-ui/core/CardHeader";
import CardContent from "@material-ui/core/CardContent";
import IconButton from "@material-ui/core/IconButton";
import Typography from "@material-ui/core/Typography";
import ReviewStatus from "../../widgets/ReviewStatus";
import ReviewValidationIcons from "../../widgets/ReviewValidationIcons";
import { trimLongReview } from "./utils";
import CropFreeIcon from "@material-ui/icons/CropFree";
import Button from "@material-ui/core/Button";
import ReviewPopUp from "./ReviewPopUp";

const useStyles = makeStyles((theme) => ({
  root: {
    maxWidth: "100%",
  },
  iconAlignment: {
    position: "absolute",
    right: "10px",
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
  iconColor: {
    color: "black",
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

const Review = ({ review }) => {
  const classes = useStyles();
  const [openReviewPopUp, setOpenReviewPopUp] = useState(false);

  const timestamp = new Date(review.timestamp);

  return (
    <Card className={classes.root} variant="outlined">
      <CardHeader
        title={
          <Typography className={classes.timeFont}>
            {timestamp.toLocaleString()}
            <Button
              type="button"
              size="small"
              className={classes.iconAlignment}
              onClick={() => setOpenReviewPopUp(true)}
            >
              {review.comments.includes("\n") ? (
                <CropFreeIcon fontSize="small" style={{ color: "blue" }} />
              ) : (
                <React.Fragment />
              )}
            </Button>
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
        <div>
          <Typography noWrap>
            {review.comments.includes("\n")
              ? `${trimLongReview(review.comments)}...`
              : review.comments}
          </Typography>
        </div>
      </CardContent>
      <IconButton disabled>
        <ReviewStatus status={review.status} />
      </IconButton>
      <IconButton disabled className={classes.iconColor}>
        <ReviewValidationIcons review={review} />
      </IconButton>
      <ReviewPopUp
        openReviewPopUp={openReviewPopUp}
        setOpenReviewPopUp={setOpenReviewPopUp}
        review={review}
      ></ReviewPopUp>
    </Card>
  );
};

export default Review;
