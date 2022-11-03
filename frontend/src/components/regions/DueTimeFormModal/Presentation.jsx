import React, { useState } from "react";
import { makeStyles } from "@material-ui/core/styles";
import Paper from "@material-ui/core/Paper";
import Button from "@material-ui/core/Button";
import DateTimePicker from "react-datetime-picker";
import Modal from "../../widgets/Modal";

const useStyles = makeStyles({
  buttons: {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
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
  handleClose,
  handleSubmit,
  loading,
}) {
  const classes = useStyles();
  const [dueTime, setDueTime] = useState(cards.dueTime);
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
                  onClick={() => handleSubmit(dueTime)}
                  loading={loading}
                >
                  Save
                </Button>
                <Button
                  className={classes.dueTimeButton}
                  variant="outlined"
                  onClick={handleClose}
                  loading={false}
                >
                  Close
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
