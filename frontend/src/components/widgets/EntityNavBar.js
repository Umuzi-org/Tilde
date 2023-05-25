import React from "react";
import { Link } from "react-router-dom";

import { Toolbar } from "@material-ui/core";

import { makeStyles } from "@material-ui/core/styles";
import Tabs from "@material-ui/core/Tabs";
import Tab from "@material-ui/core/Tab";

const useStyles = makeStyles((theme) => ({
  toolbar: {
    margin: theme.spacing(0.5),
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

export default ({ toolbarContents, tabs, selectedTab }) => {
  const classes = useStyles();
  return (
    <React.Fragment>
      <Toolbar variant="dense" className={classes.toolbar}>
        {toolbarContents}
      </Toolbar>
      <Tabs value={selectedTab} className={classes.tabs}>
        {tabs.map((tab) => (
          <Link to={tab.to} key={tab.to}>
            <Tab label={tab.label} />
          </Link>
        ))}
      </Tabs>
    </React.Fragment>
  );
};
