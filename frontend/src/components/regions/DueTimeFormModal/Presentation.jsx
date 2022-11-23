import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Paper from "@material-ui/core/Paper";
import Button from "../../widgets/Button";
import DateTimePicker from "react-datetime-picker";
import Modal from "../../widgets/Modal";
import { Typography } from "@material-ui/core";

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
    display: "flex",
    padding: "32px",
    gap: "16px",
  },
  exitIcon: {
    position: "relative",
    top: 0,
    left: "200px",
  },
  dateTimePicker: {
    minHeight: "40px",
    width: "100%",
  },
  form: {
    display: "flex",
    flexDirection: "column",
    gap: "16px",
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
            <form noValidate className={classes.form}>
              <Typography variant="h6">Set due time</Typography>
              <DateTimePicker
                onChange={setDueTime}
                value={dueTime}
                disableClock
                className={classes.dateTimePicker}
              />
              <div className={classes.buttons}>
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
              </div>
            </form>
          ) : (
            <div>Loading...</div>
          )}
        </Paper>
      </Modal>
    );
  return <React.Fragment />;
}
