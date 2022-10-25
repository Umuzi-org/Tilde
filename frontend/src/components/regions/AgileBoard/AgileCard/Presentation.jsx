import React from "react";
import Chip from "@material-ui/core/Chip";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import Typography from "@material-ui/core/Typography";
import { makeStyles } from "@material-ui/core/styles";
import AssistantPhotoIcon from "@material-ui/icons/AssistantPhoto";
import AccessAlarms from "@material-ui/icons/AccessAlarms";
import CardBadges from "../../../widgets/CardBadges";
import { BLOCKED } from "../../../../constants";
import Checkbox from "@material-ui/core/Checkbox";
// import StoryPoints from "../../../widgets/StoryPoints";
import TagChips from "../../../widgets/TagChips";
import FlavourChips from "../../../widgets/FlavourChips";
import blue from "@material-ui/core/colors/blue";
import orange from "@material-ui/core/colors/orange";
import AgileCardActions from "./AgileCardActions";
import {
  checkIfCardIsInReviewColumn,
  userReviewedSinceLastReviewRequest,
} from "./utils";

const useStyles = makeStyles((theme) => {
  const card = {
    margin: theme.spacing(1),
    backgroundColor: blue[100],
    // "border-left": `1em solid ${blue[500]}`,
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
  const title = {
    marginLeft: "10px",
    marginTop: "8px",
  };
  return {
    card,
    goalCard,
    title,
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
  const classes = useStyles();
  return (
    <Typography className={classes.title}>{userNames.join(", ")}</Typography>
  );
}

export default function Presentation({
  card,
  authUser,
  viewedUser,
  filterUserId,
  repoUrl,

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
}) {
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
    repoUrl,

    loadingStartProject,
    loadingStartTopic,
    loadingClickOpenWorkshopAttendanceForm,
    loadingRequestReview,
    loadingCancelReviewRequest,
    loadingStopTopic,
    loadingFinishTopic,
    loadingRemoveWorkshopAttendance,
  };
  //AgileCard 

  
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
        <Typography variant="caption" className={classes.title}>
          {card.contentTypeNice} {card.projectSubmissionTypeNice}
        </Typography>
        {checkIfCardIsInReviewColumn({ card }) ? (
          <Checkbox
            checked={userReviewedSinceLastReviewRequest({ viewedUser, card })}
            style={{ color: "#3f51b5" }}
            disabled
          />
        ) : (
          <React.Fragment />
        )}

        <Typography variant="h6" component="h2" className={classes.title}>
          {card.title}
        </Typography>

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
        {/* <StoryPoints storyPoints={card.storyPoints} /> */}

        <Typography variant="subtitle2" className={classes.title}>
          Assignees:
        </Typography>

        <ListCardUsers
          userNames={card.assigneeNames}
          userIds={card.assigneeIds}
        />

        {card.reviewerNames.length ? (
          <React.Fragment>
            <Typography variant="subtitle2" className={classes.title}>
              Reviewers:
            </Typography>

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
}
