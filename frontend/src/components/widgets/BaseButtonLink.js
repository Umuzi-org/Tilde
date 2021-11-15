import React from "react";
import { Link } from "react-router-dom";
import { makeStyles } from "@material-ui/core/styles";
import { Button } from "@material-ui/core";
export const useStyles = makeStyles({
  title: {
    marginTop: "8px",
    marginLeft: "16px",
  },
  input: {
    width: "62%",
  },
});
export default ({ to, label, selected }) => {
  const classes = useStyles();
  const variant = selected ? "contained" : "outlined";
  return (
    <Link to={to}>
      <Button size="small" variant={variant} className={classes.title}>
        {label}
      </Button>
    </Link>
  );
};
