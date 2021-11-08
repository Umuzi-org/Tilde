import React from "react";
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import ListItemText from "@material-ui/core/ListItemText";
import { makeStyles } from "@material-ui/core/styles";
import Drawer from "@material-ui/core/Drawer";
import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import Typography from "@material-ui/core/Typography";
import IconButton from "@material-ui/core/IconButton";
import clsx from "clsx";
import CssBaseline from "@material-ui/core/CssBaseline";
import Divider from "@material-ui/core/Divider";
import MenuIcon from "@material-ui/icons/Menu";
import Badge from "@material-ui/core/Badge";
import PersonIcon from "@material-ui/icons/Person";
import MenuItem from "@material-ui/core/MenuItem";
import Menu from "@material-ui/core/Menu";
import ChevronLeftIcon from "@material-ui/icons/ChevronLeft";
import ListItemIcon from "@material-ui/core/ListItemIcon";
import Tooltip from "@material-ui/core/Tooltip";
import { Link } from "react-router-dom";

import AddCardReviewModal from "../AddCardReviewModal";

import Avatar from "@material-ui/core/Avatar";

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
