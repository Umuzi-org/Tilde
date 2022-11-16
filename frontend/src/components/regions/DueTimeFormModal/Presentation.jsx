import React, { useState } from "react";
import { makeStyles } from "@material-ui/core/styles";
import Paper from "@material-ui/core/Paper";
import Button from "../../widgets/Button";
import DateTimePicker from "react-datetime-picker";
import Modal from "../../widgets/Modal";

const useStyles = makeStyles({
  buttons: {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
  },
  dueTimeButton: {
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
  dateTimePicker: {
    width: "100%",
  },
});

export default function Presentation({
  cards,
  cardId,
  dueTime,
  setDueTime,
  handleClose,
  handleSubmit,
}) {
  const classes = useStyles();
  if (cardId)
    return (
      <Modal open={true} onClose={handleClose}>
        <Paper className={classes.paper}>
          {cards ? (
            <form noValidate>
              <DateTimePicker
                onChange={setDueTime}
                value={dueTime}
                disableClock
                className={classes.dateTimePicker}
              />
              <p className={classes.buttons}>
                <Button
                  className={classes.dueTimeButton}
                  variant="outlined"
                  onClick={handleClose}
                >
                  Close
                </Button>
                <Button
                  className={classes.dueTimeButton}
                  variant="outlined"
                  onClick={() => handleSubmit(dueTime)}
                >
                  Save
                </Button>
              </p>
            </form>
          ) : (
            <div>Loading...</div>
          )}
        </Paper>
      </Modal>
    );
  return <React.Fragment />;
}
