import React from "react";
import { makeStyles } from "@mui/material/styles";
import Popover from "@mui/material/Popover";
// import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import HelpIcon from "@mui/icons-material/Help";

const useStyles = makeStyles((theme) => ({
  button: {
    margin: theme.spacing(1),
  },
}));

export default function Help({ buttonText, children }) {
  const classes = useStyles();
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
        className={classes.button}
      >
        {buttonText ? buttonText : "help"}
      </Button>
      <Popover
        id={id}
        open={open}
        anchorEl={anchorEl}
        onClose={handleClose}
        anchorOrigin={{
          vertical: "bottom",
          horizontal: "center",
        }}
        transformOrigin={{
          vertical: "top",
          horizontal: "center",
        }}
      >
        {children}
      </Popover>
    </div>
  );
}
