import React from "react";
import {
  Paper,
  Table,
  TableBody,
  TableRow,
  TableCell,
  Typography,
} from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";

import TagChips from "../../widgets/TagChips";
import FlavourChips from "../../widgets/FlavourChips";
import StoryPoints from "../../widgets/StoryPoints";

import Modal from "../../widgets/Modal";

import ProjectDetails from "./ProjectDetails";
import UsersTable from "./UsersTable";
import Reviews from "./Reviews";

const useStyles = makeStyles((theme) => ({
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
}));

const TopicProgressDetails = ({ topicProgress, reviews }) => {
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
};

const CardBasicDetails = ({ card }) => {
  const classes = useStyles();

  const dueTime = card.dueTime && new Date(card.dueTime).toLocaleString();
  const startTime = card.startTime && new Date(card.startTime).toLocaleString();
  const reviewRequestTime =
    card.reviewRequestTime && new Date(card.reviewRequestTime).toLocaleString();
  const completeTime =
    card.completeTime && new Date(card.completeTime).toLocaleString();

  return (
    <React.Fragment>
      <Typography variant="h5">
        {card.contentTypeNice}: {card.title}
      </Typography>
      <TagChips tagNames={card.tagNames} />
      <FlavourChips flavourNames={card.flavourNames} />
      <StoryPoints storyPoints={card.storyPoints} />

      <Paper className={classes.sectionPaper} variant="outlined">
        <Typography variant="subtitle2">Assignees:</Typography>
        <UsersTable userNames={card.assigneeNames} userIds={card.assignees} />
        <Typography variant="subtitle2">Reviewers:</Typography>
        <UsersTable userNames={card.reviewerNames} userIds={card.reviewers} />
      </Paper>

      <Paper className={classes.sectionPaper} variant="outlined">
        <Table>
          <TableBody>
            <TableRow>
              <TableCell>Due Time</TableCell>
              <TableCell>{dueTime}</TableCell>
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
    </React.Fragment>
  );
};

export default ({
  card,
  cardId,
  topicProgress,
  //   workshopAttendance,
  handleClose,
  project,
  topicReviews,
  projectReviews,
  handleClickAddReview,
  handleClickUpdateProjectLink,
  showUpdateProjectLinkForm,
  showAddReviewButton,
  linkSubmission,
  formErrors,
}) => {
  const classes = useStyles();

  const workshopAttendance = false;
  if (cardId)
    return (
      <Modal open={true} onClose={handleClose}>
        <Paper className={classes.paper}>
          {card ? <CardBasicDetails card={card} /> : <div>Loading...</div>}

          {project ? (
            <ProjectDetails
              project={project}
              handleClickUpdateProjectLink={handleClickUpdateProjectLink}
              showUpdateProjectLinkForm={showUpdateProjectLinkForm}
              linkSubmission={linkSubmission}
              formErrors={formErrors}
              showAddReviewButton={showAddReviewButton}
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
        </Paper>
      </Modal>
    );
  return <React.Fragment />;
};
