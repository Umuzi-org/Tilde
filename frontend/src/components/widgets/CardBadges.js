import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Badge from "@material-ui/core/Badge";

import SentimentVerySatisfiedIcon from "@material-ui/icons/SentimentVerySatisfied";
import SentimentSatisfiedIcon from "@material-ui/icons/SentimentSatisfied";
import SentimentDissatisfiedIcon from "@material-ui/icons/SentimentDissatisfied";
import CallMergeIcon from "@material-ui/icons/CallMerge";
import MoodBadIcon from "@material-ui/icons/MoodBad";
import { Chip, Tooltip } from "@material-ui/core";

const useStyles = makeStyles((theme) => ({
  root: {
    "& > *": {
      margin: theme.spacing(1),
    },
  },
}));

export const CompetentIcon = SentimentSatisfiedIcon;
export const ExcellentIcon = SentimentVerySatisfiedIcon;
export const NotYetCompetentIcon = SentimentDissatisfiedIcon;
export const RedFlagIcon = MoodBadIcon;

export const statusIcons = {
  C: CompetentIcon,
  E: ExcellentIcon,
  R: RedFlagIcon,
  NYC: NotYetCompetentIcon,
};

export default ({ card }) => {
  const classes = useStyles();

  const {
    codeReviewCompetentSinceLastReviewRequest,
    codeReviewExcellentSinceLastReviewRequest,
    codeReviewNyCompetentSinceLastReviewRequest,
    codeReviewRedFlagSinceLastReviewRequest,
    openPrCount,
    oldestOpenPrUpdatedTime,
  } = card;

  let ageOfOpenPR = () => {
    let date2 = new Date();
    let date1 = new Date(oldestOpenPrUpdatedTime);
    let numberOfDays = Math.floor((Math.abs(date2-date1)) / (1000 * 60 * 60 * 24));

    if(numberOfDays == 0 || numberOfDays == 1) {return `${numberOfDays} day ago`}
    else {return `${numberOfDays} days ago`}
  }

  return (
    <div className={classes.root}>
      {codeReviewCompetentSinceLastReviewRequest ? (
        <Tooltip title="Number of COMPETENT code reviews since your last review request">
          <Badge
            badgeContent={codeReviewCompetentSinceLastReviewRequest}
            color="primary"
          >
            <CompetentIcon />
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
            <ExcellentIcon />
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
            <NotYetCompetentIcon />
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
            <RedFlagIcon />
          </Badge>
        </Tooltip>
      ) : (
        <React.Fragment />
      )}

      {openPrCount ? (
        <Tooltip title="Number of open pull requests on this card and their age">
          <Badge badgeContent={openPrCount} color="primary">
            <Chip
              avatar={<CallMergeIcon />}
              className={classes.chip}
              label={ageOfOpenPR()}
            />
          </Badge>
        </Tooltip>
      ) : (
        <React.Fragment />
      )}
    </div>
  );
};
