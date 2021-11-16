import React from "react";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemText from "@mui/material/ListItemText";
import { makeStyles } from "@mui/material/styles";
import Drawer from "@mui/material/Drawer";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import IconButton from "@mui/material/IconButton";
import clsx from "clsx";
import CssBaseline from "@mui/material/CssBaseline";
import Divider from "@mui/material/Divider";
import MenuIcon from "@mui/icons-material/Menu";
import Badge from "@mui/material/Badge";
import PersonIcon from "@mui/icons-material/Person";
import MenuItem from "@mui/material/MenuItem";
import Menu from "@mui/material/Menu";
import ChevronLeftIcon from "@mui/icons-material/ChevronLeft";
import ListItemIcon from "@mui/material/ListItemIcon";
import Tooltip from "@mui/material/Tooltip";
import { Link } from "react-router-dom";

import AddCardReviewModal from "../AddCardReviewModal";

import Avatar from "@mui/material/Avatar";

const drawerWidth = 240;
const useStyles = makeStyles((theme) => {
  return {
    root: {
      display: "flex",
    },
    toolbar: {
      paddingRight: 24,
    },
    toolbarIcon: {
      display: "flex",
      alignItems: "center",
      justifyContent: "flex-end",
      padding: "0 8px",
      ...theme.mixins.toolbar,
    },
    appBar: {
      zIndex: theme.zIndex.drawer + 1,
      transition: theme.transitions.create(["width", "margin"], {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.leavingScreen,
      }),
    },
    appBarShift: {
      marginLeft: drawerWidth,
      width: `calc(100% - ${drawerWidth}px)`,
      transition: theme.transitions.create(["width", "margin"], {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.enteringScreen,
      }),
    },
    menuButton: {
      marginRight: 36,
    },
    menuButtonHidden: {
      display: "none",
    },
    title: {
      flexGrow: 1,
    },
    drawerPaper: {
      position: "relative",
      whiteSpace: "nowrap",
      width: drawerWidth,
      transition: theme.transitions.create("width", {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.enteringScreen,
      }),
    },
    drawerPaperClose: {
      overflowX: "hidden",
      transition: theme.transitions.create("width", {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.leavingScreen,
      }),
      width: theme.spacing(7),
      [theme.breakpoints.up("sm")]: {
        width: theme.spacing(0),
      }
    },
    appBarSpacer: { ...theme.mixins.toolbar },

    childContainer: {
      height: `calc(100% - ${
        theme.mixins.toolbar.minHeight
      }px - ${theme.spacing(1)}px)`,
      overflow: "auto",
      paddingTop: theme.spacing(1),
      paddingBottom: theme.spacing(4),
    },

    content: {
      flexGrow: 1,
      height: "100vh",
      overflow: "auto",
    },
    paper: {
      padding: theme.spacing(2),
      display: "flex",
      overflow: "auto",
      flexDirection: "column",
    },

    avatar: {
      width: theme.spacing(20),
      height: theme.spacing(20),
    },
  };
});

export default function Presentation(props) {
  const classes = useStyles();

  const {
    sliderMenuRoutes,
    handleOpenSlider,
    handleCloseSlider,
    anchorElementProfileMenu,
    setAnchorElementProfileMenu,
    handleLogoutClick,
    authUser,
  } = props;

  const menuItems = Object.keys(sliderMenuRoutes).map((routeName) => {
    const Icon = sliderMenuRoutes[routeName].sliderNavigation.icon;
    return (
      <Tooltip
        title={sliderMenuRoutes[routeName].sliderNavigation.helpText}
        key={routeName}
      >
        <ListItem component={Link} to={sliderMenuRoutes[routeName].route.path}>
          <ListItemIcon>
            <Avatar>
              <Icon />
            </Avatar>
          </ListItemIcon>
          <ListItemText>
            {sliderMenuRoutes[routeName].sliderNavigation.label}
          </ListItemText>
        </ListItem>
      </Tooltip>
    );
  });

  return (
    <div className={classes.root}>
      <CssBaseline />
      <AddCardReviewModal />
      {/* <MarkSingleCardAttendanceModal /> */}

      <AppBar
        position="absolute"
        className={clsx(
          classes.appBar,
          props.openSlider && classes.appBarShift
        )}
      >
        <Toolbar className={classes.toolbar}>
          <IconButton
            edge="start"
            color="inherit"
            aria-label="open drawer"
            className={clsx(
              classes.menuButton,
              props.openSlider && classes.menuButtonHidden
            )}
            onClick={handleOpenSlider}
          >
            <MenuIcon />
          </IconButton>

          <Typography
            component="h1"
            variant="h6"
            color="inherit"
            noWrap
            className={classes.title}
          >
            Tilde
          </Typography>

          {/* <IconButton color="inherit">
            <Badge badgeContent={4} color="secondary">
              <NotificationsIcon />
            </Badge>
          </IconButton> */}

          {authUser.email}

          <IconButton
            color="inherit"
            onClick={(event) => {
              setAnchorElementProfileMenu(event.currentTarget);
            }}
          >
            <Badge color="secondary">
              <PersonIcon />
            </Badge>
          </IconButton>

          <Menu
            id="profile-menu"
            anchorEl={anchorElementProfileMenu}
            keepMounted
            open={Boolean(anchorElementProfileMenu)}
            onClose={() => {
              setAnchorElementProfileMenu(null);
            }}
          >
            {/* <Link to={routes.profile.route.path}>
              <MenuItem>Profile</MenuItem>
            </Link> */}
            <MenuItem onClick={handleLogoutClick}>Logout</MenuItem>
          </Menu>
        </Toolbar>
      </AppBar>
      <Drawer
        variant="permanent"
        classes={{
          paper: clsx(
            classes.drawerPaper,
            !props.openSlider && classes.drawerPaperClose
          ),
        }}
        open={props.openSlider}
      >
        <div className={classes.toolbarIcon}>
          <IconButton onClick={handleCloseSlider}>
            <ChevronLeftIcon />
          </IconButton>
        </div>
        <Divider />

        {/* <Avatar
          alt="Remy Sharp"
          src="/static/images/avatar/1.jpg"
          className={classes.avatar}
        /> */}

        {/* <Divider /> */}
        <List>{menuItems}</List>
        <Divider />
      </Drawer>

      <main className={classes.content}>
        <div className={classes.appBarSpacer} />
        {/* <Container maxWidth="lg" className={classes.container} height="100%"> */}
        <div className={classes.childContainer}>{props.children}</div>
        {/* </Container> */}
      </main>
    </div>
  );
}
