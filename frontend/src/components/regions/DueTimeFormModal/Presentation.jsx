import React, { useState } from "react";
import { makeStyles } from "@material-ui/core/styles";
import { Paper } from "@material-ui/core";
import DateTimePicker from "react-datetime-picker";
import Modal from "../../widgets/Modal";
import CardButton from "../../widgets/CardButton";

const useStyles = makeStyles({
  dueTimeButton: {
    marginRight: "0.3rem"
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

export default ({ card, cardId, handleClose, handleSubmit, loading }) => {
  const classes = useStyles();
  const [dueTime, setDueTime] = useState(card.dueTime);
  if (cardId)
    return (
      <Modal open={true} onClose={handleClose}>
        <Paper className={classes.paper}>
          {card ? (
            <form noValidate>
              <DateTimePicker
                onChange={setDueTime}
                value={dueTime}
                disableClock
                className={classes.dateTimePicker}
              />
              <p>
                <CardButton
                  className={classes.dueTimeButton}
                  variant="outlined"
                  onClick={() => handleSubmit(dueTime)}
                  loading={loading}
                  label="Save"
                >
                  Save
                </CardButton>
                <CardButton
                  className={classes.dueTimeButton}
                  variant="outlined"
                  onClick={handleClose}
                  loading={false}
                  label="Cancel"
                >
                  Close
                </CardButton>
              </p>
            </form>
          ) : (
            <div>Loading...</div>
          )}
        </Paper>
      </Modal>
    );
  return <React.Fragment />;
};
