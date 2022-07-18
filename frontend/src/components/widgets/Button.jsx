import React from "react";
import Button from "@material-ui/core/Button";
import { makeStyles } from "@material-ui/core/styles";
import LaunchIcon from "@material-ui/icons/Launch";

const useStyles = makeStyles((theme) => ({
  button: {
    // color: "red",
    border: "1px solid grey",
    borderRadius: theme.spacing(0.5),
    borderColor: theme.palette.grey[500],
  },
}));

export default ({ children }) => {
  const classes = useStyles();
  console.log(Button);
  return (
    <Button className={classes.button} displayName={"display"} startIcon={""}>
      {children}
    </Button>
  );
};
