import React from "react";

import Button from "@mui/material/Button";
import Grid from "@mui/material/Grid";
import { makeStyles } from "@mui/material/styles";
import Loading from "./Loading";
const useStyles = makeStyles((theme) => {
  return {
    button: {
      paddingBottom: theme.spacing(0.3),
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
