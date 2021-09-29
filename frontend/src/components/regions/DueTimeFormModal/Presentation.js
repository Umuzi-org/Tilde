import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import {
  TextField,
  Button,
  Grid,
  Paper,
} from "@material-ui/core";
import Modal from '../../widgets/Modal';

const useStyles = makeStyles({

    dueTimeButton: {
        marginTop: "0.3rem",
        marginRight: "0.3rem",
    },

    paper: {
      padding: "1rem"
    }
});

const DueTimeFormModal = ({ card, closeModal }) => {

  const dueTime = card.dueTime;
  // const dueTime = "";
  /* dueTime is either an empty string or something like this: "2021-06-14T09:58:28Z".
     If dueTime has a value, then we strip out the seconds, 
     hence dueTime.split('').slice(0, 16).join('') is used */
  const defaultValue = dueTime ? dueTime.split('').slice(0, 16).join('') : "";
  const classes = useStyles();

  return (
    <Modal open={!!card} onClose={closeModal}>
      <Paper className={classes.paper}>
        <form novalidate>
          <TextField
            id="datetime-local"
            label="Due Date"
            type="datetime-local"
            defaultValue={defaultValue}
            InputLabelProps={{
              shrink: true,
            }}
          />
          <Grid container>
            <Button className={classes.dueTimeButton} variant="outlined">Save</Button>
            <Button className={classes.dueTimeButton} variant="outlined">Cancel</Button>
          </Grid>
        </form> 
      </Paper>
    </Modal>
  )
}

export default DueTimeFormModal;
