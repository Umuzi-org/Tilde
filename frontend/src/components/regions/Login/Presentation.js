import React from "react";
import { makeStyles } from "@material-ui/core";
import TextField from "@material-ui/core/TextField";
import Button from "@material-ui/core/Button";
import Typography from "@material-ui/core/Typography";
import Alert from "@material-ui/lab/Alert";
import LockRoundedIcon from "@material-ui/icons/LockRounded";

const useStyles = makeStyles((theme) => ({
  root: {
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    alignItems: "center",
    padding: theme.spacing(2),
    height: "100vh",
    overflow: "hidden",

    "& .MuiTextField-root": {
      margin: theme.spacing(1),
      width: "300px",
    },
    "& .MuiButtonBase-root": {
      margin: theme.spacing(2),
    },
  },
  alert: {
    margin: theme.spacing(1),
    width: "275px",
  },
}));

const LoginForm = ({ loading, error, handleLoginWithGoogle }) => {
  const classes = useStyles();

  return (
    <form className={classes.root}>
      <Typography variant="h5" style={{ fontWeight: 600 }}>
        Please Login
      </Typography>

      <Alert severity="info" className={classes.alert}>
        Note that this site uses popups for authentication
      </Alert>
      {error && (
        <Alert severity="error" className={classes.alert}>
          ERROR: {error}. You might need to refresh this page to attempt to
          login again
        </Alert>
      )}
      <LockRoundedIcon />
      <TextField label="Email" variant="outlined" type="email" required />
      <TextField label="Password" variant="outlined" type="password" required />
      <div>
        <Button type="submit" variant="contained" color="primary">
          Login
        </Button>
        <Button
          type="submit"
          variant="contained"
          color="primary"
          onClick={handleLoginWithGoogle}
        >
          Login with Google
        </Button>
      </div>
    </form>
  );
};

export default LoginForm;
