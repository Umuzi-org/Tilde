import React from "react";
import Button from "@material-ui/core/Button";
import { makeStyles } from "@material-ui/core/styles";
import TextField from "@material-ui/core/TextField";
import Typography from "@material-ui/core/Typography";

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

export default function ({
  handleSubmit,
  handleInputChange,
  loading,
  formErrors,
}) {
  const classes = useStyles();
  return (
    <form className={classes.containerStyles}>
      <Typography variant="h5" style={{ fontWeight: 600 }}>
        Reset Password
      </Typography>
      {/* <Alert severity="info" className={classes.alert}>
        Reset your password with the form below
      </Alert> */}

      <TextField
        margin="normal"
        required
        fullWidth
        name="newPassword1"
        label="New password"
        type="password"
        onChange={handleInputChange}
        error={Boolean(formErrors.newPassword1)}
        helperText={formErrors.newPassword1}
        variant="outlined"
      />

      <TextField
        margin="normal"
        required
        fullWidth
        name="newPassword2"
        label="Confirm password"
        type="password"
        onChange={handleInputChange}
        error={Boolean(formErrors.newPassword2)}
        helperText={formErrors.newPassword2}
        variant="outlined"
      />
      <Button
        type="submit"
        variant="contained"
        className={classes.buttonStyle}
        disabled={loading}
        onClick={handleSubmit}
      >
        Update Password
      </Button>
    </form>
  );
}
