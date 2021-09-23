import React from "react";
import { makeStyles } from "@material-ui/core";
import TextField from "@material-ui/core/TextField";
import Button from "@material-ui/core/Button";
import Typography from "@material-ui/core/Typography";
import Alert from "@material-ui/lab/Alert";

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
  button: {
    width: "300px"
  }
}));

export default () => {
  const classes = useStyles();

  return (
    <form className={classes.root}>
      <Typography variant="h5" style={{ fontWeight: 600 }}>
        Create new password
      </Typography>
      <Alert severity="info" className={classes.alert}>
        Your new password must be different from previous used passwords
      </Alert>
      <TextField label="Password" variant="outlined" type="password" required />
      <TextField
        label="Confirm Password"
        variant="outlined"
        type="password"
        required
      />
      <div>
        <Button type="submit" variant="contained" color="primary" className={classes.button}>
          Reset Password
        </Button>
      </div>
    </form>
  );
};
