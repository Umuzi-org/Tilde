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

export default ({
  card,
  cardId,
  handleClose
}) => {
  const classes = useStyles();
  // const dueTime = card.dueTime;
  const dueTime = "";
  const defaultValue = dueTime ? dueTime.split('').slice(0, 16).join('') : "";
  if (cardId)
    return (
      <Modal open={true} onClose={handleClose}>
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
    );
  return <React.Fragment />;
};
