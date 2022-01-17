import { takeLatest, put } from "redux-saga/effects";
import operations from "./operations";
import { apiReduxApps } from "../../../apiAccess/apiApps";

function* authUserResponseSideEffects(action) {
  yield put(operations.setAuthUser({ data: action.responseData }));
  yield put(
    apiReduxApps.FETCH_SINGLE_USER.operations.maybeStart({
      data: { userId: parseInt(action.responseData.userId) },
    })
  );
}

function* watchWhoAmISuccess() {
  yield takeLatest(
    apiReduxApps.WHO_AM_I.types.SUCCESS,
    authUserResponseSideEffects
  );
}

function* watchLogoutSuccess() {
  yield takeLatest(
    apiReduxApps.LOGOUT.types.SUCCESS,
    authUserResponseSideEffects
  );
}

function* watchApiAuthenticateWithOneTimeTokenSuccess() {
  yield takeLatest(
    apiReduxApps.AUTHENTICATE_WITH_ONE_TIME_TOKEN.types.SUCCESS,
    authUserResponseSideEffects
  );
}

export default [
  watchWhoAmISuccess(),
  watchLogoutSuccess(),
  watchApiAuthenticateWithOneTimeTokenSuccess(),
];
