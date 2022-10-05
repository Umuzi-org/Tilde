import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Button from "@material-ui/core/Button";
import HelpIcon from "@material-ui/icons/Help";

import Modal from "../Modal";

export default function Help({ buttonText, children }) {
  const [anchorEl, setAnchorEl] = React.useState(null);

  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const open = Boolean(anchorEl);
  const id = open ? "simple-popover" : undefined;

  return (
    <div>
      <Button
        aria-describedby={id}
        variant="outlined"
        color="primary"
        startIcon={<HelpIcon />}
        onClick={handleClick}
      >
        {buttonText ? buttonText : "help"}
      </Button>
      <Modal open={open} onClose={handleClose}>
        {children}
      </Modal>
    </div>
  );
}
