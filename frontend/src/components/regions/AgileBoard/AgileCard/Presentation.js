import React from "react";
import Chip from "@material-ui/core/Chip";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import Typography from "@material-ui/core/Typography";
import { makeStyles } from "@material-ui/core/styles";

import AssistantPhotoIcon from "@material-ui/icons/AssistantPhoto";
import AccessAlarms from "@material-ui/icons/AccessAlarms";
import MoreHorizIcon from "@material-ui/icons/MoreHoriz";

import CardReviewBadges from "../../../widgets/CardReviewBadges";

import { BLOCKED } from "../../../../constants";

import StoryPoints from "../../../widgets/StoryPoints";
import TagChips from "../../../widgets/TagChips";
import blue from "@material-ui/core/colors/blue";
import orange from "@material-ui/core/colors/orange";
import AgileCardActions from "./AgileCardActions";

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
  };

  console.log(agileCardActionProps);
  // TODO: add an icon fir different kinds of content
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
        <CardReviewBadges card={card} />
        <Typography>
          {card.contentTypeNice} {card.projectSubmissionTypeNice}
        </Typography>
        <Typography variant="caption">[card id:{card.id}]</Typography>

        <Typography variant="h5" component="h2">
          {card.title}
        </Typography>

        {card.flavourNames.map((flavour) => (
          <Chip
            key={flavour}
            className={classes.chip}
            icon={<MoreHorizIcon />}
            label={`flavour: ${flavour}`}
          />
        ))}

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
