import React, { useState } from "react";
import { makeStyles } from "@material-ui/core/styles";
import { Button, Grid, Paper } from "@material-ui/core";
import DateTimePicker from 'react-datetime-picker';
import Modal from "../../widgets/Modal";

const useStyles = makeStyles({
  dueTimeButton: {
    marginTop: "0.3rem",
    marginRight: "0.3rem",
  },
  paper: {
    padding: "1rem",
  },
  exitIcon: {
    position: "relative",
    top: 0,
    left: "200px",
  },
});

export default ({ card, cardId, handleClose }) => {
  const classes = useStyles();
  const [dueTime, setDueTime] = useState(card.dueTime);

  /* dueTime is either null or something like this: "2021-06-14T09:58:28Z".
     If dueTime has a value, then we strip out the seconds, 
     hence dueTime.split('').slice(0, 16).join('') is used */
  // const defaultValue = dueTime ? dueTime.split("").slice(0, 16).join("") : "";
  if (cardId)
    return (
      <Modal open={true} onClose={handleClose}>
        <Paper className={classes.paper}>
          {card ? (
            <form noValidate>
              <DateTimePicker onChange={setDueTime} value={dueTime} disableClock/>
              <Grid container>
                <Button className={classes.dueTimeButton} variant="outlined" onClick={() => console.log(dueTime)}>
                  Save
                </Button>
                <Button
                  className={classes.dueTimeButton}
                  variant="outlined"
                  onClick={handleClose}
                >
                  Cancel
                </Button>
              </Grid>
            </form>
          ) : (
            <div>Loading...</div>
          )}
        </Paper>
      </Modal>
    );
  return <React.Fragment />;
};
