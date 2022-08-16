import React, {useState} from "react";
import Button from "@material-ui/core/Button";
import TextField from "@material-ui/core/TextField";
import Dialog from "@material-ui/core/Dialog";
import DialogActions from "@material-ui/core/DialogActions";
import DialogContent from "@material-ui/core/DialogContent";
import DialogContentText from "@material-ui/core/DialogContentText";
import DialogTitle from "@material-ui/core/DialogTitle";
import EditTwoToneIcon from "@material-ui/icons/EditTwoTone";

export default function NickName() {
  const [open, setOpen] = useState(false);

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  return (
    <div>
        Nickname
      <Button href="#text-buttons" color="primary" onClick={handleClickOpen}>
        <EditTwoToneIcon />
      </Button>
      <Dialog
        open={open}
        onClose={handleClose}
        aria-labelledby="form-dialog-title"
      >
        <DialogTitle id="form-dialog-title">Change nick name</DialogTitle>
        <DialogContent>
          <DialogContentText>
            You are about to change your nick name. Please note that you can
            only do this once a month
          </DialogContentText>
          <TextField
            autoFocus
            margin="dense"
            id="name"
            label="New nick name"
            type="email"
            fullWidth
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose} color="primary">
            Cancel
          </Button>
          <Button onClick={handleClose} color="primary">
            Change
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}
