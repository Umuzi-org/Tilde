import React from "react";
import Grid from "@material-ui/core/Grid";
import Paper from "@material-ui/core/Paper";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableRow from "@material-ui/core/TableRow";
import TableCell from "@material-ui/core/TableCell";
import Typography from "@material-ui/core/Typography";
import CardButton from "../../widgets/CardButton";
import ViewContentButton from "../../widgets/ViewContentButton";
import { makeStyles } from "@material-ui/core/styles";
import CardStatusChip from "../../widgets/CardStatusChip";
import TagChips from "../../widgets/TagChips";
import FlavourChips from "../../widgets/FlavourChips";
// import StoryPoints from "../../widgets/StoryPoints";
import CardBadges from "../../widgets/CardBadges";
import Button from "../../widgets/Button";
import ProjectDetails from "./ProjectDetails";
import AssigneesList from "../../widgets/AssigneesList";
import ReviewersTable from "../../widgets/ReviewersTable";
import Reviews from "./Reviews";
import { canSetDueTime } from "../../regions/CardDetails/utils";

const useStyles = makeStyles((theme) => {
  return {
    paper: {
      padding: theme.spacing(1, 2, 1),
    },

    commentColumn: {
      minWidth: 300,
    },

    tableContainer: {
      maxHeight: 200,
    },
    sectionPaper: {
      padding: theme.spacing(1),
      marginBottom: theme.spacing(1),
    },
    root: {
      margin: theme.spacing(1),
      width: theme.spacing(40),
      height: theme.spacing(16),
    },
    row: {
      padding: 5,
    },
  };
});

function TopicProgressDetails({ topicProgress, reviews }) {
  return (
    <React.Fragment>
      {topicProgress.topicNeedsReview ? (
        <Reviews
          reviewIds={topicProgress.topicReviews || []}
          reviews={reviews}
        />
      ) : (
        <React.Fragment />
      )}
    </React.Fragment>
  );
}

function CardBasicDetails({
  card,
  viewedUser,
  authUser,
  handleClickSetDueTime,
}) {
  const classes = useStyles();

  const dueTime = card.dueTime && new Date(card.dueTime).toLocaleString();
  const startTime = card.startTime && new Date(card.startTime).toLocaleString();
  const reviewRequestTime =
    card.reviewRequestTime && new Date(card.reviewRequestTime).toLocaleString();
  const completeTime =
    card.completeTime && new Date(card.completeTime).toLocaleString();

  return (
    <React.Fragment>
      <Grid container>
        <Grid item xs={12} sm={12} md={12}>
          <CardBadges card={card} />
          <Typography variant="h5">
            {card.contentTypeNice}: {card.title}
          </Typography>
        </Grid>
        <Grid item xs={12} sm={12} md={12}>
          <TagChips tagNames={card.tagNames} />
          <FlavourChips flavourNames={card.flavourNames} />
          {/* <StoryPoints storyPoints={card.storyPoints} /> */}
          <CardStatusChip card={card} />
        </Grid>
        <Grid item xs={12} sm={12} md={12}>
          <Paper className={classes.sectionPaper} variant="outlined">
            <Typography variant="subtitle2">Assignees:</Typography>
            <AssigneesList
              userNames={card.assigneeNames}
              userIds={card.assignees}
            />
            <Typography variant="subtitle2">Reviewers:</Typography>
            <ReviewersTable
              reviewerUserEmails={card.reviewerNames}
              reviewerUsers={card.reviewers}
              usersThatReviewedSinceLastReviewRequestEmails={
                card.usersThatReviewedSinceLastReviewRequestEmails
              }
              usersThatReviewedSinceLastReviewRequest={
                card.usersThatReviewedSinceLastReviewRequest
              }
            />
          </Paper>
        </Grid>
        <Grid item xs={12} sm={12} md={12}>
          <Paper className={classes.sectionPaper} variant="outlined">
            <Table>
              <TableBody>
                <TableRow>
                  <TableCell>Due Time</TableCell>
                  <TableCell>
                    {dueTime}{" "}
                    {viewedUser &&
                      card.dueTime === null &&
                      canSetDueTime({ card, viewedUser, authUser }) && (
                        <Button
                          variant="outlined"
                          onClick={handleClickSetDueTime}
                        >
                          Set Time
                        </Button>
                      )}
                  </TableCell>
                </TableRow>
                {card.startTime && (
                  <TableRow>
                    <TableCell>Start Time</TableCell>
                    <TableCell>{startTime}</TableCell>
                  </TableRow>
                )}

                {card.reviewRequestTime && (
                  <TableRow>
                    <TableCell>Review Request Time</TableCell>
                    <TableCell>{reviewRequestTime}</TableCell>
                  </TableRow>
                )}
                {card.completeTime && (
                  <TableRow>
                    <TableCell>Complete Time </TableCell>
                    <TableCell>{completeTime}</TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </Paper>
        </Grid>
      </Grid>
    </React.Fragment>
  );
}

export default function Presentation({
  card,
  viewedUser,
  authUser,
  cardId,
  topicProgress,
  project,
  topicReviews,
  projectReviews,
  handleClickAddReview,
  handleClickSetDueTime,
  handleClickUpdateProjectLink,
  showUpdateProjectLinkForm,
  // showAddReviewButton,
  linkSubmission,
  formErrors,
}) {
  const classes = useStyles();

  let contentItemUrl, contentItem;
  if (card !== undefined) {
    contentItemUrl = card.contentItemUrl;
    contentItem = card.contentItem;
  }

  const workshopAttendance = false;
  if (cardId)
    return (
      <Paper className={classes.paper}>
        {card ? (
          <CardBasicDetails
            card={card}
            viewedUser={viewedUser}
            authUser={authUser}
            handleClickSetDueTime={handleClickSetDueTime}
          />
        ) : (
          <div>Loading...</div>
        )}

        {project ? (
          <ProjectDetails
            project={project}
            handleClickUpdateProjectLink={handleClickUpdateProjectLink}
            showUpdateProjectLinkForm={showUpdateProjectLinkForm}
            linkSubmission={linkSubmission}
            formErrors={formErrors}
            // showAddReviewButton={showAddReviewButton}
            handleClickAddReview={handleClickAddReview}
            reviews={projectReviews}
          />
        ) : (
          <React.Fragment />
        )}
        {topicProgress ? (
          <TopicProgressDetails
            topicProgress={topicProgress}
            reviews={topicReviews}
          />
        ) : (
          <React.Fragment />
        )}
        {workshopAttendance ? (
          // <WorkshopAttendanceDetails />
          <div>TODO: Workshop attendance details</div>
        ) : (
          <React.Fragment />
        )}

        <CardButton
          widget={
            <ViewContentButton
              contentUrl={contentItemUrl}
              contentItemId={contentItem}
            />
          }
        />
      </Paper>
    );
  return <React.Fragment />;
}
