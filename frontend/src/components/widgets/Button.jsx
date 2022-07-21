import React from "react";
import Button from "@material-ui/core/Button";
import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => ({
  button: {
    textTransform: "lowercase",
    // border: "1px solid grey",
    // borderRadius: theme.spacing(0.5),
    // borderColor: theme.palette.grey[500],
  },
}));

export default ({ children, onClick }) => {
  const classes = useStyles();
  return (
    <Button className={classes.button} onClick={onClick}>
      {children}
    </Button>
  );
};
