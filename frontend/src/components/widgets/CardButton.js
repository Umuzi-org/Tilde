import React from "react";

import Button from "@material-ui/core/Button";
import Grid from "@material-ui/core/Grid";
import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => {
  return {
    button: {
      paddingBottom: theme.spacing(0.3),
    },
  };
});

export default function CardButton({ startIcon, onClick, label, widget }) {
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
      >
        {label}
      </Button>
    );

  return (
    <Grid item xs={12} className={classes.button}>
      {inner}
    </Grid>
  );
}
