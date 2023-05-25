import types from "./types";
import { takeLeading, call, put } from "redux-saga/effects";

import { loadScript, googleAuthAvailable } from "./helpers";
import { GOOGLE_SCRIPT, GOOGLE_CLIENT_ID, GOOGLE_SCOPE } from "./consts";
import operations from "./operations";

import { apiReduxApps } from "../../apiAccess/apiApps";

const successCallbackActionCreator =
  apiReduxApps.AUTHENTICATE_WITH_ONE_TIME_TOKEN.operations.start;

function* initialiseGoogleAuthSideEffects(action) {
  try {
    if (!googleAuthAvailable()) {
      yield call(
        () =>
          new Promise((resolve) =>
            loadScript(GOOGLE_SCRIPT, () => {
              const gapi = window.gapi;
              gapi.load("auth2", () => {
                gapi.auth2.init({
                  client_id: GOOGLE_CLIENT_ID,
                  scope: GOOGLE_SCOPE,
                });
                resolve();
              });
            })
          )
      );
    }
    const ga = window.gapi.auth2.getAuthInstance();

    // const googleUser = yield call(
    //   () => new Promise((resolve, reject) => ga.signIn().then(resolve, reject))
    // );
    // const responseData = googleUser.getAuthResponse();

    const oneTimeCode = yield call(
      () =>
        new Promise((resolve, reject) =>
          ga.grantOfflineAccess().then(resolve, reject)
        )
    );

    yield put(
      operations.initialiseGoogleAuthSuccess({
        data: oneTimeCode,
      })
    );

    yield put(
      successCallbackActionCreator({
        data: { ...oneTimeCode, provider: "google" },
      })
    );
  } catch (err) {
    console.log(err);
    yield put(operations.initialiseGoogleAuthError({ error: err.error }));
  }
}

function* watchInitialiseGoogleAuthStart() {
  yield takeLeading(
    types.INITIALISE_GOOGLE_AUTH_START,
    initialiseGoogleAuthSideEffects
  );
}

// function* watchLoginWithGoogleButtonClick() {
//   yield takeLeading(
//     types.LOGIN_WITH_GOOGLE_BUTTON_CLICK,
//     loginWithGoogleButtonClickSideEffects
//   );
// }

export default [
  watchInitialiseGoogleAuthStart(),
  //   watchLoginWithGoogleButtonClick(),
];
