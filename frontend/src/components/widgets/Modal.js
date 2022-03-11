import React from "react";
import Modal from "@material-ui/core/Modal";
import Backdrop from "@material-ui/core/Backdrop";
import Fade from "@material-ui/core/Fade";
import CloseIcon from "@material-ui/icons/Close";
// import { Typography } from "@material-ui/core";

import { makeStyles } from "@material-ui/core/styles";
import { Button } from "@material-ui/core";

const useStyles = makeStyles((theme) => ({
  modal: {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
  },

  backDrop: {
    background: "rgba(0,0,0,0.15)",
  },

  exitIcon: {
    // top: "5px",
    // right: "1px",
    // backgroundColor: "white",
    // "&:hover": {
    //   backgroundColor: "white",
    // },
  },
}));

export default ({ open, onClose, children }) => {
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
      <React.Fragment>
        <Fade in={open}>{children}</Fade>
        <Button
          variant="outlined"
          onClick={onClose}
          className={classes.exitIcon}
        >
          <CloseIcon />
        </Button>
      </React.Fragment>
    </Modal>
  );
};
