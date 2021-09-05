import React, { useState } from "react";
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
import ShowMoreText from "react-show-more-text";
import ExpandLess from "@material-ui/icons/ExpandLess";
import ExpandMore from "@material-ui/icons/ExpandMore";

const useStyles = makeStyles((theme) => ({
  root: {
    maxWidth: "100%",
  },
  timeFont: {
    fontSize: 11,
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
    // "&:last-child": {
    //   paddingTop: 0,
    // }
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

  const [expand, setExpand] = useState(false);
  const onClick = () => setExpand(!expand);

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
          <Typography className={classes.cardFont}>
            {review.reviewerUserEmail}
          </Typography>
        }
        className={classes.cardHeader}
      />
      <CardContent className={classes.cardContent}>
        <Typography className={classes.cardFont}> 
          <ShowMoreText
            lines={1}
            more={<ExpandMore />}
            less={<ExpandLess />}
            onClick={onClick}
            expanded={expand}
            width={100}
            truncatedEndingComponent={`${review.comments.slice(0, review.comments.indexOf("\n"))} ... read more`}
            >
            {<Markdown children={review.comments} />}
          </ShowMoreText>
        </Typography>
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

export default Review;
