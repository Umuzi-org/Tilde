import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Badge from "@material-ui/core/Badge";

import SentimentVerySatisfiedIcon from "@material-ui/icons/SentimentVerySatisfied";
import SentimentSatisfiedIcon from "@material-ui/icons/SentimentSatisfied";
import SentimentDissatisfiedIcon from "@material-ui/icons/SentimentDissatisfied";
import MoodBadIcon from "@material-ui/icons/MoodBad";
import Tooltip from "@material-ui/core/Tooltip";

const useStyles = makeStyles((theme) => ({
  root: {
    "& > *": {
      margin: theme.spacing(1),
    },
  },
}));

export default ({ card }) => {
  const classes = useStyles();

  const {
    codeReviewCompetentSinceLastReviewRequest,
    codeReviewExcellentSinceLastReviewRequest,
    codeReviewNyCompetentSinceLastReviewRequest,
    codeReviewRedFlagSinceLastReviewRequest,
  } = card;
  return (
    <div className={classes.root}>
      {codeReviewCompetentSinceLastReviewRequest ? (
        <Tooltip title="Number of COMPETENT code reviews since your last review request">
          <Badge
            badgeContent={codeReviewCompetentSinceLastReviewRequest}
            color="primary"
          >
            <SentimentSatisfiedIcon />
          </Badge>
        </Tooltip>
      ) : (
        <React.Fragment />
      )}

      {codeReviewExcellentSinceLastReviewRequest ? (
        <Tooltip title="Number of EXCELLENT code reviews since your last review request">
          <Badge
            badgeContent={codeReviewExcellentSinceLastReviewRequest}
            color="primary"
          >
            <SentimentVerySatisfiedIcon />
          </Badge>
        </Tooltip>
      ) : (
        <React.Fragment />
      )}

      {codeReviewNyCompetentSinceLastReviewRequest ? (
        <Tooltip title="Number of NOT YET COMPETENT code reviews since your last review request">
          <Badge
            badgeContent={codeReviewNyCompetentSinceLastReviewRequest}
            color="error"
          >
            <SentimentDissatisfiedIcon />
          </Badge>
        </Tooltip>
      ) : (
        <React.Fragment />
      )}
      {codeReviewRedFlagSinceLastReviewRequest ? (
        <Tooltip title="Number of RED FLAG code reviews since your last review request">
          <Badge
            badgeContent={codeReviewRedFlagSinceLastReviewRequest}
            color="error"
          >
            <MoodBadIcon />
          </Badge>
        </Tooltip>
      ) : (
        <React.Fragment />
      )}
    </div>
  );
};
