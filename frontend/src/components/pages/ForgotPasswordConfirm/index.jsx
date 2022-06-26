import React from "react";

import { connect } from "react-redux";
import Presentation from "./Presentation.jsx";
import { REST_AUTH_BASE_URL } from "../../../config";
import { getLatestMatchingCall } from "@prelude/redux-api-toolbox/src/apiEntities/selectors";
import { useState } from "react";
import { useParams } from "react-router-dom";

import { apiReduxApps } from "@prelude/redux-api-toolbox/src/djRestAuth";
import { useApiCallbacks } from "../../../hooks";
import { useNavigate } from "react-router-dom";
import { routes } from "../../../routes";

function PasswordResetConfirmUnconnected({
  // mapStateToProps
  lastCall,

  // mapDispatchToProps
  confirmResetPassword,
}) {
  const [formData, setFormData] = useState({
    newPassword1: "",
    newPassword2: "",
  });
  const params = useParams();
  const navigate = useNavigate();

  useApiCallbacks({
    lastCallEntry: lastCall,
    successResponseCallback: () => {
      navigate(routes.login.route.path);
    },
  });
  const { token, uid } = params;

  const handleSubmit = (e) => {
    e.preventDefault();
    confirmResetPassword({ ...formData, token, uid });
  };

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const props = {
    loading: lastCall && lastCall.loading,
    formErrors:
      (lastCall && !lastCall.responseOK && lastCall.responseData) || {},
    handleSubmit,
    handleInputChange,
  };
  return <Presentation {...props} />;
}

const mapStateToProps = (state) => {
  return {
    lastCall: getLatestMatchingCall({
      state,
      BASE_TYPE: "API_PERFORM_PASSWORD_RESET",
    }),
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    confirmResetPassword: ({ newPassword1, newPassword2, token, uid }) =>
      dispatch(
        apiReduxApps.API_PERFORM_PASSWORD_RESET.operations.start({
          data: {
            REST_AUTH_BASE_URL,

            newPassword1,
            newPassword2,
            token,
            uid,
          },
        })
      ),
  };
};

const PasswordResetConfirm = connect(
  mapStateToProps,
  mapDispatchToProps
)(PasswordResetConfirmUnconnected);

export default PasswordResetConfirm;
