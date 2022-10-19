import React from "react";
import Button from "@material-ui/core/Button";
import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => ({
  button: {
    textTransform: "!important",
    border: "1px solid grey",
  },
}));

export default ({ children, onClick, startIcon }) => {
  const classes = useStyles();
  return (
    <Button className={classes.button} onClick={onClick} startIcon={startIcon}>
      {children}
    </Button>
  );
};
