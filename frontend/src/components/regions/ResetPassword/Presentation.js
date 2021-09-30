import React from "react";
import Button from "@material-ui/core/Button";
import TextField from "@material-ui/core/TextField";
import Container from "@material-ui/core/Container";
import Alert from "@material-ui/lab/Alert";

export default ({ email }) => {
  const containerStyles = {
    width: "350px",
    height: "500px",
    justifyContent: "center",
    alignItems: "center",
    textAlign: "center",
    display: "block",
    margin: "10% auto",
  };
  const textInput = {
    marginBottom: "1rem",
    width: "245px",
  };
  const alert = {
    margin: "auto",
    width: "245px",
  };
  const buttonStyle = {
    variant: "contained",
    margin: "auto",
    width: "115px",
  };
  return (
    <Container style={containerStyles}>
      <h2>Change Password</h2>
      <Alert severity="info" className={alert}>
        Please change your password below and make sure that your new password
        does not match the previous one
      </Alert>

      <form>
        <p>Email: {email}</p>
        <TextField
          style={textInput}
          label="New password"
          variant="outlined"
          type="password"
          required
        />
        <TextField
          style={textInput}
          label="Confirm new password"
          variant="outlined"
          type="password"
          required
        />
      </form>
      <Button variant="contained" color="primary" style={buttonStyle}>
        Submit
      </Button>
    </Container>
  );
};
