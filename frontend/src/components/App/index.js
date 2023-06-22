import React from "react";
import { Route, Routes, useLocation } from "react-router-dom";
import { connect } from "react-redux";

import AppHeaderAndMenu from "../regions/AppHeaderAndMenu";

import { routes } from "../../routes.js";

import { getAuthToken } from "../../utils/authTokenStorage";
import { apiReduxApps } from "../../apiAccess/apiApps";

import { createMuiTheme, ThemeProvider } from "@material-ui/core/styles";
const LogRocket = require("logrocket");

const theme = createMuiTheme({});

function shouldCallWhoAmI({ authUser }) {
  if (authUser && authUser.userId) return false;
  if (!getAuthToken()) return false;

  return true;
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

  React.useEffect(() => {
    LogRocket.identify(authUser.userId, {
      name: `${authUser.firstName} ${authUser.lastName}`,
      email: authUser.email,
    });
  }, [authUser]);

  const location = useLocation();

  const token = getAuthToken();
  const pathname = location.pathname;

  const anonymousRoutes = Object.values(routes)
    .filter((route) => route.anonymousRoute)
    .map((route) => route.matchPattern || route.route.path)
    .map((path) => pathname.match(path))
    .filter((x) => x);
  const currentlyAtAnonymousRoute = anonymousRoutes.length > 0;

  if (token === null) {
    if (!currentlyAtAnonymousRoute) {
      // this route requires login
      window.location = routes.login.route.path;
      return <React.Fragment />;
    }
  } else {
    // we are logged in
    if (currentlyAtAnonymousRoute) window.location = "/";
  }

  if (
    shouldCallWhoAmI({
      authUser: authUser,
    })
  )
    return <div>Loading...</div>;

  return (
    <ThemeProvider theme={theme}>
      <Routes>
        {Object.keys(routes).map((key) => {
          const Component = routes[key].component;
          const NavbarComponent = routes[key].navBarComponent;
          return (
            <Route
              key={key}
              {...routes[key].route}
              element={
                currentlyAtAnonymousRoute ? (
                  <Component />
                ) : (
                  <AppHeaderAndMenu>
                    {NavbarComponent && <NavbarComponent />}
                    <Component />
                  </AppHeaderAndMenu>
                )
              }
            />
          );
        })}
      </Routes>
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
