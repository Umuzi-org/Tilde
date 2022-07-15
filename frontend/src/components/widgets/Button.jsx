import React from "react";
import Button from "@material-ui/core/Button";
import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => ({
  button: {
    color: "red",
    border: "2px grey",
  },
}));

export default () => {
  const classes = useStyles();
  console.log(Button);
  return <Button className={classes.button} displayName={"display"}></Button>;
};
