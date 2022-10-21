import React from "react";
import Grid from "@material-ui/core/Grid";
import Paper from "@material-ui/core/Paper";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableRow from "@material-ui/core/TableRow";
import MuiTableCell from "@material-ui/core/TableCell";
import Typography from "@material-ui/core/Typography";
import CardButton from "../../widgets/CardButton";
import ViewContentButton from "../../widgets/ViewContentButton";
import { makeStyles, withStyles } from "@material-ui/core/styles";
import CardStatusChip from "../../widgets/CardStatusChip";
import TagChips from "../../widgets/TagChips";
import FlavourChips from "../../widgets/FlavourChips";
// import StoryPoints from "../../widgets/StoryPoints";
import CardBadges from "../../widgets/CardBadges";
import ProjectDetails from "./ProjectDetails";
import AssigneesList from "../../widgets/AssigneesList";
import ReviewersTable from "../../widgets/ReviewersTable";
import Reviews from "./Reviews";
import RateReviewRoundedIcon from "@material-ui/icons/RateReviewRounded";

const TableCell = withStyles({
  root: {
    borderBottom: "none",
  },
})(MuiTableCell);

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
      marginBottom: theme.spacing(2),
      marginTop: theme.spacing(1),
      marginRight: theme.spacing(2),
    },
    root: {
      margin: theme.spacing(1),
      width: theme.spacing(40),
      height: theme.spacing(16),
    },
    row: {
      padding: 5,
    },
    reviewers: {
      paddingTop: "3%",
    },
    addReview: {
      display: "inline-block",
      paddingTop: 5,
      paddingRight: 5,
      paddingBottom: 5,
    },
    viewContent: {
      display: "inline-block",
      padding: 5,
    },
    titleTypography: {
      [theme.breakpoints.down("md")]: {
        fontSize: "1.4rem",
      },
    },
    text: {
      [theme.breakpoints.down("md")]: {
        fontSize: "0.9rem",
      },
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

function CardBasicDetails({ card }) {
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
          <Typography variant="h5" className={classes.titleTypography}>
            {card.contentTypeNice}: {card.title}
          </Typography>
        </Grid>
        <Grid item xs={12} sm={12} md={12}>
          <TagChips tagNames={card.tagNames} />
          <FlavourChips flavourNames={card.flavourNames} />
          {/* <StoryPoints storyPoints={card.storyPoints} /> */}
          <CardStatusChip card={card} />
        </Grid>
        <Grid item xs={12} sm={12} md={6} lg={6}>
          <Paper className={classes.sectionPaper} variant="outlined">
            <Typography variant="subtitle2" className={classes.typography}>
              Assignees:
            </Typography>
            <AssigneesList
              userNames={card.assigneeNames}
              userIds={card.assignees}
            />
            <Typography variant="subtitle2" className={classes.reviewers}>
              Reviewers:
            </Typography>
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
        <Grid item xs={12} sm={12} md={6} lg={6}>
          <Paper
            className={classes.sectionPaper}
            style={{ paddingTop: "6%" }}
            elevation={0}
          >
            <Table>
              <TableBody>
                <TableRow>
                  <TableCell className={classes.text}>Due Time</TableCell>
                  <TableCell className={classes.text}>{dueTime}</TableCell>
                </TableRow>
                {card.startTime && (
                  <TableRow>
                    <TableCell className={classes.text}>Start Time</TableCell>
                    <TableCell className={classes.text}>{startTime}</TableCell>
                  </TableRow>
                )}

                {card.reviewRequestTime && (
                  <TableRow>
                    <TableCell className={classes.text}>
                      Review Request Time
                    </TableCell>
                    <TableCell className={classes.text}>
                      {reviewRequestTime}
                    </TableCell>
                  </TableRow>
                )}
                {card.completeTime && (
                  <TableRow>
                    <TableCell className={classes.text}>
                      Complete Time{" "}
                    </TableCell>
                    <TableCell className={classes.text}>
                      {completeTime}
                    </TableCell>
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
  cardId,
  topicProgress,
  project,
  topicReviews,
  projectReviews,
  handleClickAddReview,
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
        {card ? <CardBasicDetails card={card} /> : <div>Loading...</div>}

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
        <div className={classes.addReview}>
          <CardButton
            label="Add Review"
            startIcon={<RateReviewRoundedIcon />}
            onClick={handleClickAddReview}
          />
        </div>
        <div className={classes.viewContent}>
          <CardButton
            widget={
              <ViewContentButton
                contentUrl={contentItemUrl}
                contentItemId={contentItem}
              />
            }
          />
        </div>
      </Paper>
    );
  return <React.Fragment />;
}
