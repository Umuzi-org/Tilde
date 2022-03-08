import React from "react";
import { Route, useLocation } from "react-router-dom";
import { connect } from "react-redux";

import AppHeaderAndMenu from "../regions/AppHeaderAndMenu";

import { routes } from "../../routes.js";

import { getAuthToken } from "../../utils/authTokenStorage";
import { apiReduxApps } from "../../apiAccess/apiApps";

import { createMuiTheme, ThemeProvider } from "@material-ui/core/styles";

const theme = createMuiTheme({});

function shouldCallWhoAmI({ authUser }) {
  if (authUser && authUser.userId) return false;
  if (!getAuthToken()) return false;

  return true;
}

function getCurrentRoute({ location }) {
  for (let routeName in routes) {
    const route = routes[routeName];
    if (route.route.path === location.pathname) {
      return route;
    }
  }
}

function AppUnconnected({ authUser, whoAmIStart }) {
  React.useEffect(() => {
    if (
      shouldCallWhoAmI({
        authUser: authUser,
      })
    ) {
      whoAmIStart({ authUser });
    }
  }, [authUser, whoAmIStart]);

  const location = useLocation();
  const currentRoute = getCurrentRoute({ location });
  const { userMustBeLoggedIn } = currentRoute;
  const token = getAuthToken();

  if (userMustBeLoggedIn && token === null) {
    window.location = routes.login.route.path;
  }

  if (
    shouldCallWhoAmI({
      authUser: authUser,
    })
  )
    return <div>Loading...</div>;
  if (!userMustBeLoggedIn && token === null) {
    return (
      <ThemeProvider theme={theme}>
        {Object.keys(routes).map((key) => {
          return <Route key={key} {...routes[key].route} />;
        })}
      </ThemeProvider>
    );
  }
  return (
    <ThemeProvider theme={theme}>
      <AppHeaderAndMenu>
        {Object.keys(routes).map((key) => {
          return <Route key={key} {...routes[key].route} />;
        })}
      </AppHeaderAndMenu>
    </ThemeProvider>
  );
}

const mapStateToProps = (state) => {
  return { authUser: state.App.authUser, whoAmICallStatus: state.WHO_AM_I };
};

const mapDispatchToProps = (dispatch) => {
  const whoAmIStart = ({ authUser }) => {
    dispatch(
      apiReduxApps.WHO_AM_I.operations.maybeStart({ data: {}, authUser })
    );
  };

  return { whoAmIStart };
};

const App = connect(mapStateToProps, mapDispatchToProps)(AppUnconnected);

export default App;
