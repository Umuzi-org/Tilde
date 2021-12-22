import React from "react";
import { Link } from "react-router-dom";

import { Typography, Toolbar, Tooltip } from "@material-ui/core";

import { getUrl as getUserBoardUrl } from "../../widgets/LinkToUserBoard";
import { getUrl as getUserDasboardUrl } from "../../widgets/LinkToUserDashboard";
import { getUrl as getUserActionUrl } from "../../widgets/LinkToUserActions";

import GitHubIcon from "@material-ui/icons/GitHub";
import { makeStyles } from "@material-ui/core/styles";
import Tabs from "@material-ui/core/Tabs";
import Tab from "@material-ui/core/Tab";

const useStyles = makeStyles((theme) => ({
  toolbar: {
    margin: theme.spacing(0.5),
    // border: "1px solid grey",
  },
  gitHubLink: {
    margin: theme.spacing(1),
  },
  tabs: {
    "& .MuiTabs-indicator": {
      backgroundColor: "blue",
    },
  },
}));

export default ({ user, userId, value }) => {
  const classes = useStyles();
  return (
    <React.Fragment>
      <Toolbar variant="dense" className={classes.toolbar}>
        {user && <Typography>{user.email}</Typography>}
        {user && user.githubName && (
          <a
            className={classes.gitHubLink}
            href={`https://github.com/${user.githubName}`}
            target="_blank"
            rel="noopener noreferrer"
          >
            <Tooltip title={user.githubName}>
              <GitHubIcon />
            </Tooltip>
          </a>
        )}
      </Toolbar>
      <Tabs value={value} className={classes.tabs}>
        <Link to={getUserBoardUrl({ userId })}>
          <Tab label="BOARD" />
        </Link>
        <Link to={getUserActionUrl({ userId })}>
          <Tab label="ACTIONS" />
        </Link>
        <Link to={getUserDasboardUrl({ userId })}>
          <Tab label="DASHBOARD" />
        </Link>
      </Tabs>
    </React.Fragment>
  );
};
