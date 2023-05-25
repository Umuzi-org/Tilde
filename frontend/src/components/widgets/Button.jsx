import React from "react";
import Button from "@material-ui/core/Button";
import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => ({
  button: {
    textTransform: "!important",
  },
}));

export default ({ children, onClick, startIcon, variant = "outlined" }) => {
  const classes = useStyles();
  return (
    <Button
      className={classes.button}
      onClick={onClick}
      startIcon={startIcon}
      variant={variant}
    >
      {children}
    </Button>
  );
};
