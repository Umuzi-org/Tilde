import React from "react";
import Button from "@material-ui/core/Button";
import { makeStyles } from "@material-ui/core/styles";
import TextField from "@material-ui/core/TextField";
import Container from "@material-ui/core/Container";
import Alert from "@material-ui/lab/Alert";

const useStyles = makeStyles((theme) => ({
  containerStyles: {
    width: "350px",
    height: "500px",
    justifyContent: "center",
    alignItems: "center",
    textAlign: "center",
    display: "block",
    margin: "10% auto",
  },
  textInput: {
    marginBottom: "1rem",
    width: "245px",
  },
  alert: {
    margin: theme.spacing(1),
    width: "245px",
  },
  buttonStyle: {
    variant: "contained",
    margin: "auto",
    width: "115px",
  },
}));

export default ({ email }) => {
  const classes = useStyles();
  return (
    <Container className={classes.containerStyles}>
      <h2>Change Password</h2>
      <Alert severity="info" className={classes.alert}>
        Please change your password below and make sure that your new password
        does not match the previous one
      </Alert>

      <form>
        <p>Email: {email}</p>
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
      </form>
      <Button
        variant="contained"
        color="primary"
        className={classes.buttonStyle}
      >
        Submit
      </Button>
    </Container>
  );
};
