import React from "react";
import Presentation from "./Presentation";

import { authOperations } from "../../../utils/googleLogin";

import { connect } from "react-redux";

const LoginUnconnected = ({
  initialiseGoogleAuthStart,
  googleLogin,
  AUTHENTICATE_WITH_ONE_TIME_TOKEN,
}) => {
  const loginWithGoogleButtonClick = () => {
    if (!googleLogin.loading) initialiseGoogleAuthStart(googleLogin);
  };

  let error = "";
  if (
    AUTHENTICATE_WITH_ONE_TIME_TOKEN.responseData &&
    !AUTHENTICATE_WITH_ONE_TIME_TOKEN.responseOk
  ) {
    error = AUTHENTICATE_WITH_ONE_TIME_TOKEN.responseData.message;
  }

  const props = {
    handleLoginWithGoogle: loginWithGoogleButtonClick,
    loading: googleLogin.loading,
    loggedIn: googleLogin.responseData,
    error,
  };

  return <Presentation {...props} />;
};

const mapStateToProps = (state) => {
  return {
    AUTHENTICATE_WITH_ONE_TIME_TOKEN: state.AUTHENTICATE_WITH_ONE_TIME_TOKEN,
    googleLogin: state.googleLogin,
  };
};

const mapDispatchToProps = (dispatch) => {
  const initialiseGoogleAuthStart = ({ loading }) => {
    dispatch(authOperations.initialiseGoogleAuthStart({ loading }));
  };

  const loginWithGoogleButtonClick = () => {
    dispatch(authOperations.loginWithGoogleButtonClick());
  };

  return {
    initialiseGoogleAuthStart,
    loginWithGoogleButtonClick,
  };
};

const Login = connect(mapStateToProps, mapDispatchToProps)(LoginUnconnected);

export default Login;
