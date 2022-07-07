import React from "react";
import Presentation from "./Presentation";

import { authOperations } from "../../../utils/googleLogin";

import { connect } from "react-redux";

import { apiReduxApps } from "@prelude/redux-api-toolbox/src/djRestAuth";

import { REST_AUTH_BASE_URL } from "../../../config";
import { utilityOperations } from "@prelude/redux-api-toolbox/src/utilities";
import { getLatestMatchingCall } from "@prelude/redux-api-toolbox/src/apiEntities/selectors";

import { useState } from "react";

function LoginUnconnected({
  // google login
  initialiseGoogleAuthStart,
  AUTHENTICATE_WITH_ONE_TIME_TOKEN,
  googleLogin,

  // email password login
  emailPassLoginLastCall,
  doEmailPassLogin,
}) {
  const loginWithGoogleButtonClick = (e) => {
    e.preventDefault();
    if (!googleLogin.loading) initialiseGoogleAuthStart(googleLogin);
  };

  let error = "";
  if (
    AUTHENTICATE_WITH_ONE_TIME_TOKEN.responseData &&
    !AUTHENTICATE_WITH_ONE_TIME_TOKEN.responseOk
  ) {
    error = AUTHENTICATE_WITH_ONE_TIME_TOKEN.responseData.message;
  }

  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const handleSubmitLoginForm = (e) => {
    e.preventDefault();
    doEmailPassLogin(formData);
  };
  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const props = {
    handleLoginWithGoogle: loginWithGoogleButtonClick,
    googleLoginLoading: googleLogin.loading || null,
    loggedIn: googleLogin.responseData,
    error,

    // login form
    handleInputChange,
    formErrors:
      (emailPassLoginLastCall &&
        !emailPassLoginLastCall.responseOK &&
        emailPassLoginLastCall.responseData) ||
      {},
    handleSubmitLoginForm,
    loginFormLoading:
      (emailPassLoginLastCall && emailPassLoginLastCall.loading) || null,
  };

  return <Presentation {...props} />;
};

function mapStateToProps(state) {
  return {
    AUTHENTICATE_WITH_ONE_TIME_TOKEN: state.AUTHENTICATE_WITH_ONE_TIME_TOKEN,
    googleLogin: state.googleLogin,

    emailPassLoginLastCall: getLatestMatchingCall({
      state,
      BASE_TYPE: "API_LOGIN",
    }),
  };
};

const mapDispatchToProps = (dispatch) => {
  const initialiseGoogleAuthStart = ({ loading }) => {
    dispatch(authOperations.initialiseGoogleAuthStart({ loading }));
  };

  const loginWithGoogleButtonClick = () => {
    dispatch(authOperations.loginWithGoogleButtonClick());
  };

  const doEmailPassLogin = ({ email, password }) => {
    dispatch(
      apiReduxApps.API_LOGIN.operations.start({
        data: {
          REST_AUTH_BASE_URL,
          email: email,
          password: password,
        },
        successDispatchActions: [
          // apiReduxApps.API_USER_DETAILS.operations.start({
          //   data: { REST_AUTH_BASE_URL },
          // }),
          utilityOperations.pageRedirect({ url: "/" }),
        ],
      })
    );
  };

  return {
    doEmailPassLogin,
    initialiseGoogleAuthStart,
    loginWithGoogleButtonClick,
  };
};

const Login = connect(mapStateToProps, mapDispatchToProps)(LoginUnconnected);

export default Login;
