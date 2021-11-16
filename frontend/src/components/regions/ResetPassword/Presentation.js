import React from "react";
import Button from "@mui/material/Button";
import { makeStyles } from "@mui/material/styles";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import Alert from "@mui/lab/Alert";

const useStyles = makeStyles((theme) => ({
  containerStyles: {
    width: "320px",
    height: "100vh",
    justifyContent: "center",
    alignItems: "center",
    padding: theme.spacing(1),
    textAlign: "center",
    display: "block",
    margin: "10% auto",
  },
  textInput: {
    marginBottom: "1rem",
    width: "300px",
  },
  alert: {
    margin: theme.spacing(1),
    textAlign: "left",
  },
  buttonStyle: {
    variant: "contained",
    backgroundColor: "#3F51B5",
    color: "white",
    margin: "auto",
    width: "300px",
  },
  emailAddress: {
    fontFamily: "sans-serif",
  },
}));

export default ({ email }) => {
  const classes = useStyles();
  return (
    <form className={classes.containerStyles}>
      <Typography variant="h5" style={{ fontWeight: 600 }}>
        Change Password
      </Typography>
      <Alert severity="info" className={classes.alert}>
        Please change your password below and make sure that your new password
        does not match the previous one
      </Alert>

      <p className={classes.emailAddress}>Email: {email}</p>
      <TextField
        className={classes.textInput}
        label="New password"
        variant="outlined"
        type="password"
        required
      />
      <TextField
        className={classes.textInput}
        label="Confirm new password"
        variant="outlined"
        type="password"
        required
      />
      <Button variant="contained" className={classes.buttonStyle}>
        Submit
      </Button>
    </form>
  );
};
