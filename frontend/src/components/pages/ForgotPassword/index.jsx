import React, { useState } from "react";
import { connect } from "react-redux";

import Presentation from "./Presentation.jsx";

import { getLatestMatchingCall } from "@prelude/redux-api-toolbox/src/apiEntities/selectors";
import { apiReduxApps } from "@prelude/redux-api-toolbox/src/djRestAuth";

import { REST_AUTH_BASE_URL } from "../../../config";

function ForgotPasswordUnconnected({
  // mapStateToProps
  lastCall,

  // mapDispatchToProps
  resetPassword,
}) {
  const [formData, setFormData] = useState({
    email: "",
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    resetPassword(formData);
  };

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const props = {
    handleSubmit,
    handleInputChange,
    loading: lastCall && lastCall.loading,
    formErrors:
      (lastCall && !lastCall.responseOK && lastCall.responseData) || {},
    formLastSentTo:
      (lastCall && lastCall.responseOk && lastCall.requestData.email) || "",
  };
  
  return <Presentation {...props} />;
}

const mapStateToProps = (state) => {
  return {
    lastCall: getLatestMatchingCall({
      state,
      BASE_TYPE: "API_REQUEST_PASSWORD_RESET",
    }),
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    resetPassword: ({ email }) => {
      dispatch(
        apiReduxApps.API_REQUEST_PASSWORD_RESET.operations.maybeStart({
          data: {
            REST_AUTH_BASE_URL,
            email,
          },
        })
      );
    },
  };
};

const ForgotPassword = connect(
  mapStateToProps,
  mapDispatchToProps
)(ForgotPasswordUnconnected);

export default ForgotPassword;
