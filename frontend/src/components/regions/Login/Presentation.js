import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Button from "@material-ui/core/Button";
import Typography from "@material-ui/core/Typography";

import { Paper } from "@material-ui/core";
import Alert from "@material-ui/lab/Alert";

const useStyles = makeStyles((theme) => ({
  root: {
    margin: theme.spacing(2),
    // padding: theme.spacing(2),
  },
  button: {
    margin: theme.spacing(1),
  },
  alert: {
    margin: theme.spacing(1),
  },
}));

export default ({ loading, error, handleLoginWithGoogle }) => {
  const classes = useStyles();

  return (
    <Paper className={classes.root}>
      <Typography variant="h6">Please log in</Typography>

      <Alert severity="info" className={classes.alert}>
        Note that this site uses popups for authentication
      </Alert>

      {error && (
        <Alert severity="error" className={classes.alert}>
          ERROR: {error}. You might need to refresh this page to attempt to
          login again
        </Alert>
      )}

      <Button
        className={classes.button}
        variant="contained"
        onClick={handleLoginWithGoogle}
      >
        Login with Google
      </Button>
    </Paper>
  );
};
