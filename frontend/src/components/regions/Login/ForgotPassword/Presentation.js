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
  buttonDiv: {
    display: "flex",
    flexDirection: "column",
    justifyContent: "space-between",
    margin: "0px",
  },
  button: {
    width: "300px ",
    margin: "0px"
  },

}));

export default () => {
  const classes = useStyles();

  return (
    <form className={classes.root}>
      <Typography variant="h5" style={{ fontWeight: 600 }}>
        Reset password
      </Typography>

      <Alert severity="info" className={classes.alert}>
        Enter the email associated with your account and we will send an email
        with instructions to reset your password
      </Alert>

      <TextField label="Email" variant="outlined" type="email" required />

      <div className={classes.buttonDiv}>
        <Button
          className={classes.button}
          type="submit"
          variant="contained"
          color="primary"
        >
          Reset password
        </Button>
  
        <Button className={classes.button} type="submit" variant="contained" color="primary">
          Back home
        </Button>
      </div>
    </form>
  );
};
