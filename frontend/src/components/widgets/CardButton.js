import React from "react";

import Button from "@material-ui/core/Button";
import Grid from "@material-ui/core/Grid";
import { makeStyles } from "@material-ui/core/styles";
import Loading from "./Loading";
const useStyles = makeStyles((theme) => {
  return {
    button: {
      paddingBottom: theme.spacing(0.3),
      marginLeft: theme.spacing(1)
    },
  };
});

export default function CardButton({
  startIcon,
  onClick,
  label,
  widget,
  loading,
}) {
  const classes = useStyles();
  const inner =
    widget !== undefined ? (
      widget
    ) : (
      <Button
        variant="outlined"
        color="default"
        size="small"
        startIcon={startIcon}
        onClick={onClick}
        disabled={loading}
      >
        {label}
        {loading && <Loading />}
      </Button>
    );

  return (
    <Grid item xs={12} className={classes.button}>
      {inner}
    </Grid>
  );
}
