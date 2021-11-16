import React from "react";
import Chip from "@mui/material/Chip";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import { makeStyles } from "@mui/material/styles";

import AssistantPhotoIcon from "@mui/icons-material/AssistantPhoto";
import AccessAlarms from "@mui/icons-material/AccessAlarms";

import CardBadges from "../../../widgets/CardBadges";

import { BLOCKED } from "../../../../constants";

import Checkbox from "@mui/material/Checkbox";
import StoryPoints from "../../../widgets/StoryPoints";
import TagChips from "../../../widgets/TagChips";
import FlavourChips from "../../../widgets/FlavourChips";
import blue from "@mui/material/colors/blue";
import orange from "@mui/material/colors/orange";
import AgileCardActions from "./AgileCardActions";
import {
  checkIfCardIsInReviewColumn,
  userReviewedSinceLastReviewRequest,
} from "./utils";

const useStyles = makeStyles((theme) => {
  const card = {
    margin: theme.spacing(1),
    backgroundColor: blue[100],
  };

  const goalCard = {
    ...card,
    borderWidth: theme.spacing(0.5),
    borderColor: theme.palette.primary.dark,
  };

  const blockedCard = {
    ...card,
    backgroundColor: theme.palette.grey[200],
  };

  return {
    card,
    goalCard,

    blockedCard,
    blockedGoal: {
      ...goalCard,
      ...blockedCard,
      borderColor: theme.palette.grey[800],
    },

    reviewCard: {
      // the user needs to review this
      ...card,
      //TODO
      backgroundColor: orange[100],
    },

    chip: {
      margin: theme.spacing(0.3),
    },
  };
});

const getCardClassName = ({ classes, card, filterUserId }) => {
  const isReviewer = card.reviewers.indexOf(filterUserId) !== -1;

  if (isReviewer) return classes.reviewCard;
  if (card.status === BLOCKED) {
    return card.isHardMilestone ? classes.blockedGoal : classes.blockedCard;
  }

  return card.isHardMilestone ? classes.goalCard : classes.card;
};

function ListCardUsers({ userNames, userIds }) {
  return <Typography>{userNames.join(", ")}</Typography>;
}

export default ({
  card,
  authUser,
  viewedUser,
  filterUserId,

  handleClickAddReview,
  handleClickOpenCardDetails,

  handleRequestReview,
  handleStartProject,
  handleCancelReviewRequest,

  handleClickOpenWorkshopAttendanceForm,
  handleStartTopic,
  handleStopTopic,
  handleFinishTopic,
  handleRemoveWorkshopAttendance,

  loadingStartProject,
  loadingStartTopic,
  loadingClickOpenWorkshopAttendanceForm,
  loadingRequestReview,
  loadingCancelReviewRequest,
  loadingStopTopic,
  loadingFinishTopic,
  loadingRemoveWorkshopAttendance,
}) => {
  const classes = useStyles();

  const agileCardActionProps = {
    handleClickAddReview,
    handleClickOpenCardDetails,

    handleRequestReview,
    handleStartProject,
    handleCancelReviewRequest,

    handleClickOpenWorkshopAttendanceForm,
    handleStartTopic,
    handleStopTopic,
    handleFinishTopic,
    handleRemoveWorkshopAttendance,
    card,
    authUser,
    viewedUser,

    loadingStartProject,
    loadingStartTopic,
    loadingClickOpenWorkshopAttendanceForm,
    loadingRequestReview,
    loadingCancelReviewRequest,
    loadingStopTopic,
    loadingFinishTopic,
    loadingRemoveWorkshopAttendance,
  };

  // TODO: add an icon for different kinds of content
  return (
    <Card
      className={getCardClassName({
        classes,
        card,
        filterUserId,
      })}
      variant="outlined"
    >
      <CardContent>
        <CardBadges card={card} />
        <Typography variant="caption">
          {card.contentTypeNice} {card.projectSubmissionTypeNice}
        </Typography>
        <Typography variant="caption"> [card id:{card.id}]</Typography>
        {checkIfCardIsInReviewColumn({ card }) ? (
          <Checkbox
            checked={userReviewedSinceLastReviewRequest({ viewedUser, card })}
            style={{ color: "#3f51b5" }}
            disabled
          />
        ) : (
          <React.Fragment />
        )}

        <Typography variant="h6" component="h2">
          {card.title}
        </Typography>

        {/* {card.flavourNames.map((flavour) => (
          <Chip
            key={flavour}
            className={classes.chip}
            icon={<MoreHorizIcon />}
            label={`flavour: ${flavour}`}
          />
        ))} */}

        {card.dueTime ? (
          <Chip
            className={classes.chip}
            icon={<AccessAlarms />}
            label={`Due: ${card.dueTime}`}
          />
        ) : (
          <React.Fragment />
        )}

        {card.isHardMilestone ? (
          <Chip
            className={classes.chip}
            icon={<AssistantPhotoIcon />}
            label="Goal"
          />
        ) : (
          <React.Fragment />
        )}

        <TagChips tagNames={card.tagNames} />
        <FlavourChips flavourNames={card.flavourNames} />
        <StoryPoints storyPoints={card.storyPoints} />

        <Typography variant="subtitle2">Assignees:</Typography>

        <ListCardUsers
          userNames={card.assigneeNames}
          userIds={card.assigneeIds}
        />

        {card.reviewerNames.length ? (
          <React.Fragment>
            <Typography variant="subtitle2">Reviewers:</Typography>

            <ListCardUsers
              userNames={card.reviewerNames}
              userIds={card.reviewerIds}
            />
          </React.Fragment>
        ) : (
          <React.Fragment />
        )}
      </CardContent>
      <AgileCardActions {...agileCardActionProps} />{" "}
    </Card>
  );
};
