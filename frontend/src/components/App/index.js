import React from "react";
import { BrowserRouter as Router, Route } from "react-router-dom";
import { connect } from "react-redux";

import AppHeaderAndMenu from "../regions/AppHeaderAndMenu";
import Login from "../regions/Login";

import { routes } from "../../routes.js";

import { getAuthToken } from "../../utils/authTokenStorage";
import { apiReduxApps } from "../../apiAccess/redux/apiApps";

import { createMuiTheme, ThemeProvider } from "@material-ui/core/styles";

const theme = createMuiTheme({
  // status: {
  //   danger: orange[500],
  // },
  //   palette: {
  //     type: "dark",
  //   },
});

function shouldCallWhoAmI({ authUser }) {
  if (authUser.userId) return false;
  if (!getAuthToken()) return false;
  //   if (callStatus.loading) return false;
  //   if (callStatus.error) return false;
  //   if (callStatus.responseOk) return false;
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
  });

  const token = getAuthToken();

  if (token === null) {
    return <Login />;
  }

  if (
    shouldCallWhoAmI({
      authUser: authUser,
    })
  )
    return <div>Loading...</div>;

  return (
    <Router>
      <ThemeProvider theme={theme}>
        <AppHeaderAndMenu>
          {Object.keys(routes).map((key) => {
            return <Route key={key} {...routes[key].route} />;
          })}
        </AppHeaderAndMenu>
      </ThemeProvider>
    </Router>
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
