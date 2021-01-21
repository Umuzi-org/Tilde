import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Card from "@material-ui/core/Card";
import CardActions from "@material-ui/core/CardActions";
import CardContent from "@material-ui/core/CardContent";
import Button from "@material-ui/core/Button";
import Typography from "@material-ui/core/Typography";

import { Paper } from "@material-ui/core";
import Alert from "@material-ui/lab/Alert";

// const useStyles = makeStyles({
//   root: {
//     // minWidth: 275,
//     // marginLeft: "450px",
//     // marginTop: "100px",
//     // width: "400px",
//     // height: "200px",
//   },
//   button: {
//     // marginLeft: "100px",
//     // marginTop: "5px",
//   },
// });

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

  return (
    <Card className={classes.root}>
      <CardContent>
        <Typography>Please log in. Use a Gmail registered account.</Typography>

        <br />
        <Typography>
          Note that this site uses popups for authentication.
        </Typography>

        {error && (
          <Typography>
            ERROR: {error}. You might need to refresh this page to attempt to
            login again
          </Typography>
        )}
      </CardContent>
      <CardActions>
        <Button
          className={classes.button}
          variant="contained"
          onClick={handleLoginWithGoogle}
        >
          Login with Google
        </Button>
      </CardActions>
    </Card>
  );
};

// TODO: make this look better needsissue
