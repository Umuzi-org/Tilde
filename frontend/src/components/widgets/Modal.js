import React from "react";
import Modal from "@mui/material/Modal";
import Backdrop from "@mui/material/Backdrop";
import Fade from "@mui/material/Fade";

import { makeStyles } from "@mui/material/styles";

const useStyles = makeStyles((theme) => ({
  modal: {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
  },
  backDrop: {
    background: "rgba(0,0,0,0.15)",
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
      <Fade in={open}>{children}</Fade>
    </Modal>
  );
};
