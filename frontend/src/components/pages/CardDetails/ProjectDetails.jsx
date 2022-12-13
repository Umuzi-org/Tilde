import React from "react";
import Paper from "@material-ui/core/Paper";
import Button from "@material-ui/core/Button";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import TextField from "@material-ui/core/TextField";
import { makeStyles } from "@material-ui/core/styles";
import RepositoryDetails from "./RepositoryDetails";
import CardButton from "../../widgets/CardButton";
import RateReviewRoundedIcon from "@material-ui/icons/RateReviewRounded";
import Reviews from "./Reviews";

const useStyles = makeStyles((theme) => ({
  sectionPaper: {
    padding: theme.spacing(1),
    marginBottom: theme.spacing(2),
    marginRight: theme.spacing(2),
  },
  text: {
    [theme.breakpoints.down("md")]: {
      fontSize: "0.9rem",
    },
  },
}));

function LinkToYourWork({
  currentLinkSubmission,
  handleClickUpdateProjectLink,
  showUpdateProjectLinkForm,
  linkSubmission,
  formErrors,
}) {
  const classes = useStyles();
  return (
    <Paper className={classes.sectionPaper} variant="outlined">
      <Typography variant="subtitle2" className={classes.text}>
        Link to your work:
      </Typography>

      {currentLinkSubmission ? (
        <Typography className={classes.text}>
          current value:{" "}
          <a
            href={currentLinkSubmission}
            target="_blank"
            rel="noopener noreferrer"
          >
            {currentLinkSubmission}{" "}
          </a>
        </Typography>
      ) : (
        <Typography className={classes.text}>
          Nothing submitted yet...
        </Typography>
      )}

      {showUpdateProjectLinkForm ? (
        <form noValidate onSubmit={handleClickUpdateProjectLink}>
          {formErrors}
          <Grid container spacing={1}>
            <Grid item xs={12}>
              <TextField
                id="your-link"
                label="Your Link"
                variant="outlined"
                size="small"
                {...linkSubmission}
              />
            </Grid>
            <Grid item xs={12}>
              <Button variant="outlined" size="small" type="submit">
                Update Link
              </Button>
            </Grid>
          </Grid>
        </form>
      ) : (
        <React.Fragment />
      )}
    </Paper>
  );
}

export default function Presentation({
  project,
  handleClickUpdateProjectLink,
  showUpdateProjectLinkForm,
  linkSubmission,
  formErrors,
  // showAddReviewButton,
  handleClickAddReview,
  reviews,
}) {
  const classes = useStyles();

  return (
    <React.Fragment>
      {project.repository ? (
        <Paper className={classes.sectionPaper} variant="outlined">
          <RepositoryDetails repositoryId={project.repository} />
        </Paper>
      ) : (
        <React.Fragment />
      )}

      {project.submissionTypeNice === "link" ? (
        <LinkToYourWork
          currentLinkSubmission={project.linkSubmission}
          handleClickUpdateProjectLink={handleClickUpdateProjectLink}
          showUpdateProjectLinkForm={showUpdateProjectLinkForm}
          linkSubmission={linkSubmission}
          formErrors={formErrors}
        />
      ) : (
        <React.Fragment />
      )}

      <Reviews reviewIds={project.projectReviews} reviews={reviews} />

      <CardButton
        label="Add Review"
        startIcon={<RateReviewRoundedIcon />}
        onClick={handleClickAddReview}
      />
    </React.Fragment>
  );
}
