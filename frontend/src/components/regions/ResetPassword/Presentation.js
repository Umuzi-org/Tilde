import React from "react";
import Button from "@material-ui/core/Button";
import TextField from "@material-ui/core/TextField";
import Container from "@material-ui/core/Container";

export default ({ email }) => {
  const containerStyles = {
    width: '300px',
    height: '500px',
    justifyContent: 'center',
    alignItems: 'center',
    textAlign: "center",
    display: "block",
    marginTop: "10%",
  }
  const textInput = {
    marginBottom: '1rem',
  }
  return (
    <Container style = {containerStyles}>
      <form>
        <p>Email: {email}</p>
        <TextField
        style={textInput}
          label="Password"
          variant="outlined"
          type="password"
          required
        />
        <TextField
        style={textInput}
          label="Confirm Password"
          variant="outlined"
          type="password"
          required
        />
      </form>
      <Button variant="contained" color="primary" margin="auto">
        Submit
      </Button>
    </Container>
    
  );
};

