import React from "react";
import Modal from "../../widgets/Modal";
import { Typography, Paper, Button, Grid } from "@mui/material";
import FormControl from "@mui/material/FormControl";
import Select from "@mui/material/Select";
import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import TextareaAutosize from "@mui/material/TextareaAutosize";
import Alert from "@mui/lab/Alert";

import Help from "../../widgets/Help";
import CardButton from "../../widgets/CardButton";
import SentimentVerySatisfiedIcon from "@mui/icons-material/SentimentVerySatisfied";
import SentimentSatisfiedIcon from "@mui/icons-material/SentimentSatisfied";
import SentimentDissatisfiedIcon from "@mui/icons-material/SentimentDissatisfied";
import MoodBadIcon from "@mui/icons-material/MoodBad";

import { makeStyles } from "@mui/material/styles";

const useStyles = makeStyles((theme) => ({
  formControl: {
    // margin: theme.spacing(1),
    minWidth: 120,
  },
  selectEmpty: {
    // marginTop: theme.spacing(2),
    // paddingTop: theme.spacing(2),
  },
  alert: {
    marginBottom: theme.spacing(1),
  },
  paper: {
    padding: theme.spacing(1),
  },
  textArea: {
    width: "100%",
  },
  rightButton: {
    float: "right",
  },
}));

const StatusHelp = () => {
  return (
    <Help buttonText="How do I choose a status?">
      <Paper>
        <Typography variant="subtitle2">
          <SentimentSatisfiedIcon /> Competent
        </Typography>

        <ul>
          <li>
            <Typography>
              The project matches the specification - it does what it is
              supposed to
            </Typography>
          </li>
          <li>
            <Typography>
              All the relevent code is in the master branch - The master branch
              has to work!
            </Typography>
          </li>
          <li>
            <Typography>
              The code is neat and tidy - but it doesn't have to be perfect
            </Typography>
          </li>
          <li>
            <Typography>The names used in the code make sense</Typography>
          </li>
        </ul>

        <Typography variant="subtitle2">
          <SentimentVerySatisfiedIcon /> Excellent
        </Typography>
        <ul>
          <li>
            <Typography>The code is better than competent</Typography>
          </li>
          <li>
            <Typography>
              If there were extra challenges on the project, those were
              completed and are in the master branch
            </Typography>
          </li>
          <li>
            <Typography>The code is simply beautiful to behold</Typography>
          </li>
        </ul>

        <Typography variant="subtitle2">
          <SentimentDissatisfiedIcon /> Not Yet Competent
          <ul>
            <li>
              <Typography>The code is on its way to competent</Typography>
            </li>
            <li>
              <Typography>
                The recruit(s) working on this project will be able to succeed
              </Typography>
            </li>
          </ul>
        </Typography>
        <Typography variant="subtitle2">
          <MoodBadIcon /> Red Flag
          <ul>
            <li>
              <Typography>
                There is something terribly wrong, maybe master branch is empty,
                or the recruit ignored instructions, or it is clear that the
                recruit doesn't understand the technologies in play
              </Typography>
            </li>
            <li>
              <Typography>This recruit needs some serious help</Typography>
            </li>
            <li>
              <Typography>
                Red flags are taken seriously. If someone gets a red flag then a
                staff member will intervene. So use this wisely
              </Typography>
            </li>
            <li>
              <Typography>
                If you think you can help this recruit then try to help them
                before giving them a red flag. Remember that the only meaningful
                measure of success is the number of people you have helped!
              </Typography>
            </li>
          </ul>
        </Typography>
      </Paper>
    </Help>
  );
};

export default ({
  card,
  handleSubmit,
  status,
  comments,
  formErrors,
  closeModal,
  statusChoices,
  loading,
}) => {
  const classes = useStyles();

  if (!card) {
    return <React.Fragment />;
  }

  return (
    <Modal open={!!card} onClose={closeModal}>
      <Paper className={classes.paper}>
        <Typography variant="h5">
          Add Review for {card.contentType}: {card.title}
        </Typography>

        <Alert severity="info" className={classes.alert}>
          Whatever you writ here will be visable to staff and to the person you
          are reviewing. Take the time to give an accurate and useful review
        </Alert>

        <form noValidate onSubmit={handleSubmit}>
          {formErrors}

          <Grid container spacing={1}>
            <Grid item xs={12}>
              <FormControl
                variant="outlined"
                className={classes.formControl}
                fullWidth
              >
                <InputLabel id="demo-simple-select-outlined-label" required>
                  Status
                </InputLabel>
                <Select
                  labelId="demo-simple-select-outlined-label"
                  id="demo-simple-select-outlined"
                  label="Status"
                  {...status}
                >
                  {Object.keys(statusChoices).map((key) => {
                    return (
                      <MenuItem key={key} value={key}>
                        {statusChoices[key]}
                      </MenuItem>
                    );
                  })}
                </Select>
              </FormControl>
              <StatusHelp />
            </Grid>
            <Grid item xs={12}>
              <TextareaAutosize
                className={classes.textArea}
                aria-label="your comments"
                rowsMin={5}
                placeholder="Your comments*"
                {...comments}
              />
            </Grid>
            <Grid item xs={6}>
              <Button variant="outlined" onClick={closeModal}>
                Cancel
              </Button>
            </Grid>
            <Grid item xs={6}>
              <CardButton
                type="submit"
                variant="outlined"
                className={classes.rightButton}
                loading={loading}
                label="Submit your review"
                onClick={handleSubmit}
              ></CardButton>
            </Grid>
          </Grid>
        </form>
      </Paper>
    </Modal>
  );
};
