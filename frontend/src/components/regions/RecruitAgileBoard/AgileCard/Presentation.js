import React from "react";
import Chip from "@material-ui/core/Chip";
import Grid from "@material-ui/core/Grid";
import Card from "@material-ui/core/Card";
import CardActions from "@material-ui/core/CardActions";
import CardContent from "@material-ui/core/CardContent";
import Typography from "@material-ui/core/Typography";
import { makeStyles } from "@material-ui/core/styles";

import AssistantPhotoIcon from "@material-ui/icons/AssistantPhoto";
import MoreIcon from "@material-ui/icons/More";
import PlayCircleFilledWhiteIcon from "@material-ui/icons/PlayCircleFilledWhite";
import ArrowBackRoundedIcon from "@material-ui/icons/ArrowBackRounded";
import ArrowForwardRounded from "@material-ui/icons/ArrowForwardRounded";
import RateReviewRoundedIcon from "@material-ui/icons/RateReviewRounded";
import AccessAlarms from "@material-ui/icons/AccessAlarms";
import MoreHorizIcon from "@material-ui/icons/MoreHoriz";

import CardButton from "../../../widgets/CardButton";
import CardReviewBadges from "../../../widgets/CardReviewBadges";

import {
  BLOCKED,
  //   IN_PROGRESS,
  //    READY,
  //   REVIEW_FEEDBACK,
  //   IN_REVIEW,
  //   COMPLETE,
} from "../../../../constants";

import StoryPoints from "../../../widgets/StoryPoints";
import TagChips from "../../../widgets/TagChips";
import ViewContentButton from "../../../widgets/ViewContentButton";
import blue from "@material-ui/core/colors/blue";
import orange from "@material-ui/core/colors/orange";

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

function AgileCardActions({
  card,

  handleClickOpenCardDetails,

  handleClickAddReview,
  handleRequestReview,
  handleStartProject,
  handleCancelReviewRequest,

  handleClickOpenWorkshopAttendanceForm,
  handleStartTopic,
  handleStopTopic,
  handleFinishTopic,
  handleRemoveWorkshopAttendance,

  showButtonStartProject,

  showButtonRequestReview,
  showButtonCancelReviewRequest,
  showButtonAddReview,
  showButtonStartTopic,
  showButtonStopTopic,
  showButtonEndTopic,
  showButtonNoteWorkshopAttendance,
  showButtonCancelWorkshopAttendance,
}) {
  return (
    <CardActions>
      <Grid container>
        <CardButton
          widget={
            <ViewContentButton
              contentUrl={card.contentItemUrl}
              contentItemId={card.contentItem}
            />
          }
        />

        {showButtonStartProject ? (
          <CardButton
            label="Start Project"
            startIcon={<PlayCircleFilledWhiteIcon />}
            onClick={handleStartProject}
          />
        ) : (
          ""
        )}

        <CardButton
          label="Details"
          startIcon={<MoreIcon />}
          onClick={handleClickOpenCardDetails}
        />

        {showButtonRequestReview ? (
          <CardButton
            label="Request Review"
            startIcon={<ArrowForwardRounded />}
            onClick={handleRequestReview}
          />
        ) : (
          ""
        )}

        {showButtonCancelReviewRequest ? (
          <CardButton
            label="Cancel Review Request"
            startIcon={<ArrowBackRoundedIcon />}
            onClick={handleCancelReviewRequest}
          />
        ) : (
          ""
        )}

        {showButtonAddReview ? (
          <CardButton
            label="Add Review"
            startIcon={<RateReviewRoundedIcon />}
            onClick={handleClickAddReview}
          />
        ) : (
          ""
        )}

        {showButtonStartTopic ? (
          <CardButton
            label="Start Topic"
            startIcon={<ArrowForwardRounded />}
            onClick={handleStartTopic}
          />
        ) : (
          ""
        )}

        {showButtonStopTopic ? (
          <CardButton
            label="Cancel"
            startIcon={<ArrowBackRoundedIcon />}
            onClick={handleStopTopic}
          />
        ) : (
          ""
        )}

        {showButtonEndTopic ? (
          <CardButton
            label="I'm done"
            startIcon={<ArrowForwardRounded />}
            onClick={handleFinishTopic}
          />
        ) : (
          ""
        )}

        {showButtonNoteWorkshopAttendance ? (
          <CardButton
            label="Mark Attendance"
            startIcon={<ArrowForwardRounded />}
            onClick={handleClickOpenWorkshopAttendanceForm}
          />
        ) : (
          ""
        )}

        {showButtonCancelWorkshopAttendance ? (
          <CardButton
            label="Cancel"
            startIcon={<ArrowBackRoundedIcon />}
            onClick={handleRemoveWorkshopAttendance}
          />
        ) : (
          ""
        )}
      </Grid>
    </CardActions>
  );
}

export default ({
  card,
  authUser,
  AppFilter,

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

  showButtonStartProject,
  showButtonProjectDetails,
  showButtonRequestReview,
  showButtonCancelReviewRequest,
  showButtonAddReview,

  showButtonStartTopic,
  showButtonStopTopic,
  showButtonEndTopic,

  showButtonNoteWorkshopAttendance,
  showButtonCancelWorkshopAttendance,
}) => {
  const classes = useStyles();

  return (
    <Card
      className={getCardClassName({
        classes,
        card,
        filterUserId: AppFilter.userId,
      })}
      variant="outlined"
    >
      <CardContent>
        {/* <LocalLibraryIcon /> TODO: put an icon here, different for different content types. Make it show up on the same line as the content type text*/}

        <CardReviewBadges card={card} />

        <Typography>
          {card.contentType} {card.projectSubmissionTypeNice}
        </Typography>

        <Typography variant="caption">[card id:{card.id}]</Typography>

        <Typography variant="h5" component="h2">
          {card.title}
        </Typography>

        {card.contentFlavourNames.map((flavour) => (
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

        <TagChips tags={card.tags} />
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
      <AgileCardActions
        card={card}
        authUser={authUser}
        handleClickOpenCardDetails={handleClickOpenCardDetails}
        handleClickAddReview={handleClickAddReview}
        handleRequestReview={handleRequestReview}
        handleStartProject={handleStartProject}
        handleCancelReviewRequest={handleCancelReviewRequest}
        showButtonStartProject={showButtonStartProject}
        showButtonProjectDetails={showButtonProjectDetails}
        showButtonRequestReview={showButtonRequestReview}
        showButtonCancelReviewRequest={showButtonCancelReviewRequest}
        showButtonAddReview={showButtonAddReview}
        showButtonStartTopic={showButtonStartTopic}
        showButtonStopTopic={showButtonStopTopic}
        showButtonEndTopic={showButtonEndTopic}
        showButtonNoteWorkshopAttendance={showButtonNoteWorkshopAttendance}
        showButtonCancelWorkshopAttendance={showButtonCancelWorkshopAttendance}
        handleClickOpenWorkshopAttendanceForm={
          handleClickOpenWorkshopAttendanceForm
        }
        handleStartTopic={handleStartTopic}
        handleStopTopic={handleStopTopic}
        handleFinishTopic={handleFinishTopic}
        handleRemoveWorkshopAttendance={handleRemoveWorkshopAttendance}
      />
    </Card>
  );
};
