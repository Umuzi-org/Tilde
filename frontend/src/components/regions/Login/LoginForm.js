import React, { useState } from "react";
import { makeStyles } from "@material-ui/core";
import TextField from "@material-ui/core/TextField";
import Button from "@material-ui/core/Button";

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
}));

const LoginForm = () => {
  const classes = useStyles();

  return (
    <form className={classes.root}>
      <TextField label="Email" variant="outlined" type="email" required />
      <TextField label="Password" variant="outlined" type="password" required />
      <div>
        <Button type="submit" variant="contained" color="primary">
          Login
        </Button>
      </div>
    </form>
  );
};

export default LoginForm;
