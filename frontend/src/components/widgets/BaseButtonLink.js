import React from "react";
import { Link } from "react-router-dom";
import { makeStyles } from "@material-ui/core/styles";
import Button from "./Button";
const useStyles = makeStyles({
  marginsAlignment: {
    marginTop: "8px",
    marginLeft: "16px",
  },
});
export default ({ to, label, selected }) => {
  const classes = useStyles();
  const variant = selected ? "contained" : "outlined";
  return (
    <Link to={to}>
      <Button
        size="small"
        variant={variant}
        className={classes.marginsAlignment}
      >
        {label}
      </Button>
    </Link>
  );
};
