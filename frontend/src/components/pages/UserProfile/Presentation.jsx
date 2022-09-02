import React from "react";

import Grid from "@material-ui/core/Grid";
import Paper from "@material-ui/core/Paper";
import Avatar from "@material-ui/core/Avatar";
import Button from "@material-ui/core/Button";
import { makeStyles } from "@material-ui/core/styles";
import Typography from "@material-ui/core/Typography";
import ButtonGroup from "@material-ui/core/ButtonGroup";
import AddAPhotoOutlinedIcon from "@material-ui/icons/AddAPhotoOutlined";
import GitHubIcon from "@material-ui/icons/GitHub";
import MailIcon from "@material-ui/icons/Mail";
import useMediaQuery from "@material-ui/core/useMediaQuery";
// To get the rocket chat icon
import { Icon } from "@iconify/react";

import NickName from "./NickName";

const useStyles = makeStyles((theme) => ({
  root: {
    maxHeight: "90vh",
    maxWidth: "90vw",
    display: "flex",
    flexFlow: "row nowrap",
    alignItems: "center",
    justifyContent: "center",
  },
  grid: {
    width: "70%",
    height: "70%",
    position: "relative",
    top: 100,
  },
  paperStyle: {
    padding: theme.spacing(0),
    textAlign: "center",
    color: theme.palette.text.secondary,
    height: "40vh",
    display: "flex",
    flexFlow: "row nowrap",
    justifyContent: "center",
    alignItems: "center",
    textTransform: "none",
    position: "relative",
  },
  avatar: {
    width: "100%",
    height: "100%",
  },
  button: {
    color: "white",
    backgroundColor: "#ff9800",
    position: "absolute",
    bottom: 10,
    right: 10,
    zIndex: 2,
  },
  textStyle: {
    color: "black",
    textTransform: "none",
  },
  forgotPassword: {
    color: "#ff9800",
    position: "absolute",
    bottom: 10,
    right: 10,
  },
}));

export default function UserProfile() {
  const classes = useStyles();
  const mobile = useMediaQuery("(min-width:600px");

  return (
    <div className={classes.root}>
      <Grid
        className={classes.grid}
        container="true"
        spacing={0}
        direction="row"
        justifyContent="center"
        alignItems="center"
      >
        <Grid item xs={12} md={6} lg={6}>
          <Paper className={classes.paperStyle} elevation={6}>
            <Avatar
              src="https://cdn.dribbble.com/users/4307805/screenshots/15598347/media/a6be63d86327c045f08e58e6b26084c7.png?compress=1&resize=400x300"
              alt="profile picture"
              variant="rounded"
              className={classes.avatar}
            />
            <div>
              <Button onClick={this} className={classes.button}>
                <AddAPhotoOutlinedIcon />
              </Button>
            </div>
          </Paper>
        </Grid>
        <Grid item xs={12} md={6} lg={6}>
          <Paper className={classes.paperStyle} elevation={6}>
            <div style={{ position: "absolute", top: 30 }}>
              <Typography variant="h3">
                Student Full Name
                <Typography variant="h5">
                  <NickName />
                </Typography>
              </Typography>
            </div>
            <div className={classes.root}>
              <ButtonGroup
                orientation={`${mobile ? "horizontal" : "vertical"}`}
                aria-label="text primary button group"
                variant="outlined"
                size={`${mobile ? "large" : "small"}`}
              >
                <Button className={classes.textStyle}>
                  <div>
                    <div>RocketChat name</div>
                    <div>
                      <Icon icon="logos:rocket-chat-icon" />
                    </div>
                  </div>
                </Button>
                <Button className={classes.textStyle}>
                  <div>
                    <div>Github name</div>
                    <div>
                      <GitHubIcon />
                    </div>
                  </div>
                </Button>
                <Button className={classes.textStyle}>
                  <div>
                    <div>Email address</div>
                    <div>
                      <MailIcon />
                    </div>
                  </div>
                </Button>
              </ButtonGroup>
            </div>
            <Typography className={classes.forgotPassword}>
              <div>forgot password ?</div>
            </Typography>
          </Paper>
        </Grid>
      </Grid>
    </div>
  );
}
