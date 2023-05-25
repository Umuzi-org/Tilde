import React from "react";
import Modal from "@material-ui/core/Modal";
import Paper from "@material-ui/core/Paper";
import Backdrop from "@material-ui/core/Backdrop";
import Fade from "@material-ui/core/Fade";
import { makeStyles } from "@material-ui/core/styles";
import Typography from "@material-ui/core/Typography";
import Grid from "@material-ui/core/Grid";
import CloseIcon from "@material-ui/icons/Close";
import IconButton from "@material-ui/core/IconButton";

const useStyles = makeStyles((theme) => ({
  modal: {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
  },

  backDrop: {
    background: "rgba(0,0,0,0.15)",
  },

  paper: {
    padding: theme.spacing(2),
  },

  modalHeadingSection: {
    marginBottom: theme.spacing(1),
  },

  exitIconContainer: {
    display: "flex",
    justifyContent: "flex-end",
    height: "0%",
  },
}));

export default ({ open, onClose, children, title }) => {
  const classes = useStyles();

  return (
    <Modal
      aria-labelledby="transition-modal-title"
      aria-describedby="transition-modal-description"
      className={classes.modal}
      open={open}
      onClose={onClose}
      closeAfterTransition
      BackdropComponent={Backdrop}
      BackdropProps={{
        timeout: 500,
        classes: {
          root: classes.backDrop,
        },
      }}
    >
      <Fade in={open}>
        <Paper className={classes.paper}>
          <Grid container className={classes.modalHeadingSection}>
            <Grid item xs={10}>
              <Typography variant="h5">{title}</Typography>
            </Grid>
            <Grid item xs={2} className={classes.exitIconContainer}>
              <IconButton
                children={<CloseIcon />}
                className={classes.exitIcon}
                onClick={onClose}
              />
            </Grid>
          </Grid>

          {children}
        </Paper>
      </Fade>
    </Modal>
  );
};
