import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Help from "../../widgets/Help";
import SentimentVerySatisfiedIcon from "@material-ui/icons/SentimentVerySatisfied";
import SentimentSatisfiedIcon from "@material-ui/icons/SentimentSatisfied";
import SentimentDissatisfiedIcon from "@material-ui/icons/SentimentDissatisfied";
import MoodBadIcon from "@material-ui/icons/MoodBad";
import Paper from "@material-ui/core/Paper";
import Typography from "@material-ui/core/Typography";

const useStyles = makeStyles({
  paperStyle: {
    maxHeight: "80vh",
    maxWidth: "80vw",
    overflow: "auto",
    padding: "5px",
  },
});

export default function StatusHelp() {
  const classes = useStyles();
  return (
    <Help buttonText="How do I choose a status?">
      <Paper className={classes.paperStyle}>
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
              All the relevant code is in the master branch - The master branch
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
}
